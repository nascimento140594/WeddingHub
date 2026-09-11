from decimal import Decimal

from django.db import transaction

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, authentication_classes
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Payment
from .serializers import CheckoutSerializer, PaymentSerializer
from .services import (
    MercadoPagoAPIError,
    MercadoPagoConfigurationError,
    create_preference,
    get_payment,
    normalize_amount,
    validate_webhook_signature,
)


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    queryset = Payment.objects.select_related(
        "gift",
        "gift__wedding",
    )

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = [
        "status",
    ]

    search_fields = [
        "guest_name",
        "guest_email",
        "transaction_id",
    ]

    ordering_fields = [
        "amount",
        "created_at",
        "guest_name",
        "status",
    ]

    ordering = [
        "-created_at",
    ]

    def get_queryset(self):
        return self.queryset.filter(
            gift__wedding__owner=self.request.user
        )

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[AllowAny],
        authentication_classes=[],
        url_path="checkout",
    )
    def checkout(self, request):
        """Create a public Mercado Pago Checkout Pro payment."""
        serializer = CheckoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        gift = serializer.validated_data["gift"]

        payment = Payment.objects.create(
            gift=gift,
            guest_name=serializer.validated_data["guest_name"],
            guest_email=serializer.validated_data["guest_email"],
            amount=gift.price,
            status=Payment.Status.PENDING,
        )

        try:
            preference = create_preference(payment)
        except MercadoPagoConfigurationError as exc:
            payment.delete()
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        except MercadoPagoAPIError as exc:
            payment.delete()
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        payment.transaction_id = preference.get("id", "")
        payment.save(update_fields=["transaction_id"])

        return Response(
            {
                "payment_id": payment.id,
                "preference_id": preference.get("id"),
                "checkout_url": preference.get("init_point"),
                "status": payment.status,
            },
            status=status.HTTP_201_CREATED,
        )


@api_view(["POST"])
@authentication_classes([])
def mercadopago_webhook(request):
    """Receive and validate Mercado Pago payment notifications."""
    data_id = request.query_params.get("data.id")

    if not data_id:
        return Response(
            {"detail": "Missing data.id."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not validate_webhook_signature(request, data_id):
        return Response(
            {"detail": "Invalid webhook signature."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    try:
        mercado_pago_payment = get_payment(data_id)
    except MercadoPagoConfigurationError as exc:
        return Response(
            {"detail": str(exc)},
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )
    except MercadoPagoAPIError as exc:
        return Response(
            {"detail": str(exc)},
            status=status.HTTP_502_BAD_GATEWAY,
        )

    external_reference = mercado_pago_payment.get("external_reference")

    if not external_reference:
        return Response(
            {"detail": "Payment has no external reference."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        with transaction.atomic():
            payment = Payment.objects.select_for_update().select_related(
                "gift"
            ).get(pk=external_reference)

            local_amount = normalize_amount(payment.amount)
            remote_amount = normalize_amount(
                mercado_pago_payment.get("transaction_amount", 0)
            )

            if local_amount != remote_amount:
                return Response(
                    {"detail": "Payment amount does not match."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            remote_status = mercado_pago_payment.get("status")
            status_map = {
                "approved": Payment.Status.PAID,
                "pending": Payment.Status.PENDING,
                "in_process": Payment.Status.PENDING,
                "rejected": Payment.Status.FAILED,
                "cancelled": Payment.Status.FAILED,
                "refunded": Payment.Status.REFUNDED,
                "charged_back": Payment.Status.REFUNDED,
            }
            new_status = status_map.get(
                remote_status,
                Payment.Status.PENDING,
            )

            old_status = payment.status
            payment.status = new_status
            payment.transaction_id = str(data_id)
            payment.save(update_fields=["status", "transaction_id"])

            if (
                new_status == Payment.Status.PAID
                and old_status != Payment.Status.PAID
            ):
                gift = payment.gift
                if gift.reserved < gift.quantity:
                    gift.reserved += 1
                    gift.save(update_fields=["reserved"])

            if (
                new_status == Payment.Status.REFUNDED
                and old_status == Payment.Status.PAID
            ):
                gift = payment.gift
                if gift.reserved > 0:
                    gift.reserved -= 1
                    gift.save(update_fields=["reserved"])

    except Payment.DoesNotExist:
        return Response(
            {"detail": "Local payment not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    return Response(
        {"received": True},
        status=status.HTTP_200_OK,
    )
