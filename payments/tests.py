from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from gifts.models import Gift
from payments.models import Payment
from wedding.models import Wedding

User = get_user_model()


class PaymentTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="matheus@example.com",
            password="12345678",
        )

        self.other_user = User.objects.create_user(
            email="outro@example.com",
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

        self.other_wedding = Wedding.objects.create(
            owner=self.other_user,
            title="Outro Casamento",
            bride_name="Maria",
            groom_name="José",
            wedding_date="2027-11-20",
            ceremony_time="18:00:00",
            ceremony_address="Rua A",
            reception_address="Salão B",
            city="Curitiba",
            state="PR",
        )

        self.gift = Gift.objects.create(
            wedding=self.wedding,
            name="Geladeira",
            description="Geladeira Brastemp",
            price="3500.00",
            quantity=1,
        )

        self.other_gift = Gift.objects.create(
            wedding=self.other_wedding,
            name="Fogão",
            description="Fogão 5 bocas",
            price="2500.00",
            quantity=1,
        )

        self.client.force_authenticate(self.user)

    def payment_data(self):
        return {
            "gift": self.gift.id,
            "guest_name": "João da Silva",
            "guest_email": "joao@email.com",
            "amount": "3500.00",
            "status": "PENDING",
            "transaction_id": "TX123456",
        }

    def test_create_payment(self):
        url = reverse("payment-list")

        response = self.client.post(
            url,
            self.payment_data(),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            Payment.objects.count(),
            1,
        )

    def test_list_only_own_payments(self):
        Payment.objects.create(
            gift=self.gift,
            guest_name="João",
            guest_email="joao@email.com",
            amount="3500.00",
            status="PENDING",
        )

        Payment.objects.create(
            gift=self.other_gift,
            guest_name="Maria",
            guest_email="maria@email.com",
            amount="2500.00",
            status="PAID",
        )

        url = reverse("payment-list")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

    def test_search_payment(self):
        Payment.objects.create(
            gift=self.gift,
            guest_name="João da Silva",
            guest_email="joao@email.com",
            amount="3500.00",
            status="PENDING",
        )

        url = reverse("payment-list")

        response = self.client.get(
            url,
            {
                "search": "João",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

    def test_filter_status(self):
        Payment.objects.create(
            gift=self.gift,
            guest_name="João",
            guest_email="joao@email.com",
            amount="3500.00",
            status="PAID",
        )

        url = reverse("payment-list")

        response = self.client.get(
            url,
            {
                "status": "PAID",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

    def test_update_payment(self):
        payment = Payment.objects.create(
            gift=self.gift,
            guest_name="João",
            guest_email="joao@email.com",
            amount="3500.00",
            status="PENDING",
        )

        url = reverse(
            "payment-detail",
            args=[payment.id],
        )

        response = self.client.patch(
            url,
            {
                "status": "PAID",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        payment.refresh_from_db()

        self.assertEqual(
            payment.status,
            "PAID",
        )

    def test_delete_payment(self):
        payment = Payment.objects.create(
            gift=self.gift,
            guest_name="João",
            guest_email="joao@email.com",
            amount="3500.00",
            status="PENDING",
        )

        url = reverse(
            "payment-detail",
            args=[payment.id],
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

    def test_ordering_amount(self):
        Payment.objects.create(
            gift=self.gift,
            guest_name="João",
            guest_email="joao@email.com",
            amount="1000.00",
            status="PENDING",
        )

        Payment.objects.create(
            gift=self.gift,
            guest_name="Carlos",
            guest_email="carlos@email.com",
            amount="5000.00",
            status="PENDING",
        )

        url = reverse("payment-list")

        response = self.client.get(
            url,
            {
                "ordering": "-amount",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data[0]["guest_name"],
            "Carlos",
        )
