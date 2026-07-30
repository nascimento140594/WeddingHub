from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated

from .models import Payment
from .serializers import PaymentSerializer


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
