from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class RegisterUserTests(APITestCase):
    def test_register_user_success(self):
        url = reverse("accounts:register")

        payload = {
            "email": "matheus@example.com",
            "first_name": "Matheus",
            "last_name": "Nascimento",
            "phone": "11999999999",
            "password": "12345678",
            "password_confirm": "12345678",
        }

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            User.objects.filter(
                email="matheus@example.com"
            ).exists()
        )

    def test_register_user_password_mismatch(self):
        url = reverse("accounts:register")

        payload = {
            "email": "matheus@example.com",
            "first_name": "Matheus",
            "last_name": "Nascimento",
            "phone": "11999999999",
            "password": "12345678",
            "password_confirm": "87654321",
        }

        response = self.client.post(url, payload, format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_register_duplicate_email(self):
        User.objects.create_user(
            email="matheus@example.com",
            password="12345678",
        )

        url = reverse("accounts:register")

        payload = {
            "email": "matheus@example.com",
            "first_name": "Matheus",
            "last_name": "Nascimento",
            "phone": "11999999999",
            "password": "12345678",
            "password_confirm": "12345678",
        }

        response = self.client.post(url, payload, format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )


class JWTAuthenticationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="matheus@example.com",
            password="12345678",
        )

    def test_login_returns_tokens(self):
        url = reverse("token_obtain_pair")

        payload = {
            "email": "matheus@example.com",
            "password": "12345678",
        }

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_invalid_credentials(self):
        url = reverse("token_obtain_pair")

        payload = {
            "email": "matheus@example.com",
            "password": "wrongpassword",
        }

        response = self.client.post(url, payload, format="json")

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )


class MeEndpointTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="matheus@example.com",
            password="12345678",
            first_name="Matheus",
        )

    def test_me_requires_authentication(self):
        url = reverse("accounts:me")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_me_returns_authenticated_user(self):
        self.client.force_authenticate(self.user)

        url = reverse("accounts:me")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["email"],
            self.user.email,
        )
