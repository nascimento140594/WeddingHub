from decimal import Decimal

from django.db.models import Count, Sum
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from gifts.models import Gift
from guestbook.models import GuestMessage
from guests.models import Guest
from payments.models import Payment


class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wedding = request.user.wedding

        total_guests = Guest.objects.filter(
            wedding=wedding,
        ).count()

        confirmed = Guest.objects.filter(
            wedding=wedding,
            status=Guest.Status.CONFIRMED,
        ).count()

        declined = Guest.objects.filter(
            wedding=wedding,
            status=Guest.Status.DECLINED,
        ).count()

        pending = Guest.objects.filter(
            wedding=wedding,
            status=Guest.Status.PENDING,
        ).count()

        total_gifts = Gift.objects.filter(
            wedding=wedding,
        ).count()

        reserved = Gift.objects.filter(
            wedding=wedding,
            reserved__gt=0,
        ).count()

        total_payments = Payment.objects.filter(
            gift__wedding=wedding,
        ).count()

        amount = (
            Payment.objects.filter(
                gift__wedding=wedding,
                status=Payment.Status.PAID,
            ).aggregate(
                total=Sum("amount")
            )["total"]
            or Decimal("0.00")
        )

        messages = GuestMessage.objects.filter(
            wedding=wedding,
        ).count()

        return Response(
            {
                "total_guests": total_guests,
                "confirmed_guests": confirmed,
                "declined_guests": declined,
                "pending_guests": pending,
                "total_gifts": total_gifts,
                "reserved_gifts": reserved,
                "total_payments": total_payments,
                "amount_received": amount,
                "messages": messages,
            }
        )
