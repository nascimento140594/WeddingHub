from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from guests.models import Guest
from wedding.models import Wedding

User = get_user_model()


class GuestTests(APITestCase):
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
            wedding_date="2027-11-01",
            ceremony_time="18:00:00",
            ceremony_address="Rua A",
            reception_address="Salão B",
            city="Curitiba",
            state="PR",
        )

        self.client.force_authenticate(self.user)

    def guest_data(self):
        return {
            "full_name": "João da Silva",
            "email": "joao@email.com",
            "phone": "11999999999",
            "invitation_code": "CONVITE001",
            "companions": 2,
            "notes": "Amigo da família",
        }

    def test_create_guest(self):
        url = reverse("guest-list")

        response = self.client.post(
            url,
            self.guest_data(),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            Guest.objects.count(),
            1,
        )

        self.assertEqual(
            Guest.objects.first().wedding,
            self.wedding,
        )

    def test_list_only_own_guests(self):
        Guest.objects.create(
            wedding=self.wedding,
            **self.guest_data(),
        )

        Guest.objects.create(
            wedding=self.other_wedding,
            full_name="Outro Convidado",
            email="outro@email.com",
            phone="111111111",
            invitation_code="OUTRO001",
        )

        url = reverse("guest-list")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

    def test_confirm_guest(self):
        guest = Guest.objects.create(
            wedding=self.wedding,
            **self.guest_data(),
        )

        url = reverse(
            "guest-confirm",
            args=[guest.id],
        )

        response = self.client.post(
            url,
            {
                "companions": 3,
                "message": "Confirmado!",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        guest.refresh_from_db()

        self.assertEqual(
            guest.status,
            Guest.Status.CONFIRMED,
        )

        self.assertEqual(
            guest.companions,
            3,
        )

    def test_decline_guest(self):
        guest = Guest.objects.create(
            wedding=self.wedding,
            **self.guest_data(),
        )

        url = reverse(
            "guest-decline",
            args=[guest.id],
        )

        response = self.client.post(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        guest.refresh_from_db()

        self.assertEqual(
            guest.status,
            Guest.Status.DECLINED,
        )

    def test_filter_guest_by_status(self):
        Guest.objects.create(
            wedding=self.wedding,
            status=Guest.Status.CONFIRMED,
            **self.guest_data(),
        )

        url = reverse("guest-list")

        response = self.client.get(
            url,
            {
                "status": "CONFIRMED",
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
