from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from guestbook.models import GuestMessage
from wedding.models import Wedding

User = get_user_model()


class GuestbookTests(APITestCase):
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

        self.client.force_authenticate(self.user)

    def message_data(self):
        return {
            "wedding": self.wedding.id,
            "guest_name": "Carlos Oliveira",
            "guest_email": "carlos@email.com",
            "message": "Desejo muitas felicidades ao casal!",
        }

    def test_create_message(self):
        url = reverse("guestbook-list")

        response = self.client.post(
            url,
            self.message_data(),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            GuestMessage.objects.count(),
            1,
        )

    def test_list_only_own_messages(self):
        GuestMessage.objects.create(
            wedding=self.wedding,
            guest_name="Carlos",
            guest_email="carlos@email.com",
            message="Parabéns!",
        )

        GuestMessage.objects.create(
            wedding=self.other_wedding,
            guest_name="Maria",
            guest_email="maria@email.com",
            message="Felicidades!",
        )

        url = reverse("guestbook-list")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

    def test_search_message(self):
        GuestMessage.objects.create(
            wedding=self.wedding,
            guest_name="Carlos Oliveira",
            guest_email="carlos@email.com",
            message="Parabéns!",
        )

        url = reverse("guestbook-list")

        response = self.client.get(
            url,
            {
                "search": "Carlos",
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

    def test_filter_approved(self):
        GuestMessage.objects.create(
            wedding=self.wedding,
            guest_name="Carlos",
            guest_email="carlos@email.com",
            message="Parabéns!",
            approved=True,
        )

        url = reverse("guestbook-list")

        response = self.client.get(
            url,
            {
                "approved": True,
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

    def test_update_message(self):
        message = GuestMessage.objects.create(
            wedding=self.wedding,
            guest_name="Carlos",
            guest_email="carlos@email.com",
            message="Parabéns!",
        )

        url = reverse(
            "guestbook-detail",
            args=[message.id],
        )

        response = self.client.patch(
            url,
            {
                "message": "Muitas felicidades!",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        message.refresh_from_db()

        self.assertEqual(
            message.message,
            "Muitas felicidades!",
        )

    def test_delete_message(self):
        message = GuestMessage.objects.create(
            wedding=self.wedding,
            guest_name="Carlos",
            guest_email="carlos@email.com",
            message="Parabéns!",
        )

        url = reverse(
            "guestbook-detail",
            args=[message.id],
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertEqual(
            GuestMessage.objects.count(),
            0,
        )

    def test_ordering_guest_name(self):
        GuestMessage.objects.create(
            wedding=self.wedding,
            guest_name="Ana",
            guest_email="ana@email.com",
            message="Mensagem",
        )

        GuestMessage.objects.create(
            wedding=self.wedding,
            guest_name="Carlos",
            guest_email="carlos@email.com",
            message="Mensagem",
        )

        url = reverse("guestbook-list")

        response = self.client.get(
            url,
            {
                "ordering": "guest_name",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data[0]["guest_name"],
            "Ana",
        )
