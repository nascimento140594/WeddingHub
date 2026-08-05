from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from wedding.models import Wedding

User = get_user_model()


class WeddingTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="matheus@example.com",
            password="12345678",
        )

        self.other_user = User.objects.create_user(
            email="outro@example.com",
            password="12345678",
        )

        self.client.force_authenticate(self.user)

    def wedding_data(self):
        return {
            "title": "Casamento Matheus & Laura",
            "bride_name": "Laura",
            "groom_name": "Matheus",
            "wedding_date": "2027-12-18",
            "ceremony_time": "16:00:00",
            "ceremony_address": "Rua das Flores, 100",
            "reception_address": "Salão Imperial",
            "city": "São Paulo",
            "state": "SP",
            "about": "Nosso grande dia",
            "primary_color": "#C8A97E",
            "secondary_color": "#FFFFFF",
            "instagram_hashtag": "#LauraEMatheus",
            "pix_key": "pix@email.com",
            "is_public": True,
        }

    def test_create_wedding(self):
        url = reverse("wedding:create")

        response = self.client.post(
            url,
            self.wedding_data(),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(Wedding.objects.count(), 1)
        self.assertEqual(Wedding.objects.first().owner, self.user)

    def test_get_own_wedding(self):
        Wedding.objects.create(
            owner=self.user,
            **self.wedding_data(),
        )

        url = reverse("wedding:detail")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["bride_name"],
            "Laura",
        )

    def test_update_wedding(self):
        Wedding.objects.create(
            owner=self.user,
            **self.wedding_data(),
        )

        url = reverse("wedding:detail")

        payload = {
            "city": "Rio de Janeiro",
        }

        response = self.client.patch(
            url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        wedding = Wedding.objects.get(owner=self.user)

        self.assertEqual(
            wedding.city,
            "Rio de Janeiro",
        )

    def test_user_cannot_access_other_wedding(self):
        Wedding.objects.create(
            owner=self.other_user,
            **self.wedding_data(),
        )

        url = reverse("wedding:detail")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )
