from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from gifts.models import Gift
from guestbook.models import GuestMessage
from guests.models import Guest
from payments.models import Payment
from wedding.models import Wedding

User = get_user_model()


class DashboardTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="matheus@example.com",
            password="12345678",
        )

        self.wedding = Wedding.objects.create(
            owner=self.user,
            title="Casamento Matheus & Laura",
            bride_name="Laura",
            groom_name="Matheus",
            wedding_date="2027-12-18",
            ceremony_time="16:00:00",
            ceremony_address="Rua das Flores, 100",
            reception_address="Salão Imperial",
            city="São Paulo",
            state="SP",
        )

        self.client.force_authenticate(self.user)

        self.gift = Gift.objects.create(
            wedding=self.wedding,
            name="Geladeira",
            description="Geladeira Brastemp",
            price="3500.00",
            quantity=1,
            reserved=1,
        )

        Guest.objects.create(
            wedding=self.wedding,
            full_name="João",
            email="joao@email.com",
            invitation_code="CONV001",
            status=Guest.Status.CONFIRMED,
        )

        Guest.objects.create(
            wedding=self.wedding,
            full_name="Maria",
            email="maria@email.com",
            invitation_code="CONV002",
            status=Guest.Status.PENDING,
        )

        Guest.objects.create(
            wedding=self.wedding,
            full_name="Carlos",
            email="carlos@email.com",
            invitation_code="CONV003",
            status=Guest.Status.DECLINED,
        )

        Payment.objects.create(
            gift=self.gift,
            guest_name="João",
            guest_email="joao@email.com",
            amount="3500.00",
            status=Payment.Status.PAID,
        )

        GuestMessage.objects.create(
            wedding=self.wedding,
            guest_name="João",
            guest_email="joao@email.com",
            message="Parabéns!",
            approved=True,
        )

    def test_dashboard_requires_authentication(self):
        self.client.force_authenticate(user=None)

        url = reverse("dashboard")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_dashboard_statistics(self):
        url = reverse("dashboard")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["total_guests"],
            3,
        )

        self.assertEqual(
            response.data["confirmed_guests"],
            1,
        )

        self.assertEqual(
            response.data["declined_guests"],
            1,
        )

        self.assertEqual(
            response.data["pending_guests"],
            1,
        )

        self.assertEqual(
            response.data["total_gifts"],
            1,
        )

        self.assertEqual(
            response.data["reserved_gifts"],
            1,
        )

        self.assertEqual(
            response.data["total_payments"],
            1,
        )

        # Corrigido para aceitar o Decimal retornado pelo DRF
        self.assertEqual(
            float(response.data["amount_received"]),
            3500.0,
        )

        self.assertEqual(
            response.data["messages"],
            1,
        )
