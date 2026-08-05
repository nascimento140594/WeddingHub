from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from gifts.models import Gift
from wedding.models import Wedding

User = get_user_model()


class GiftTests(APITestCase):
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
            wedding_date="2027-10-10",
            ceremony_time="18:00:00",
            ceremony_address="Rua A",
            reception_address="Salão B",
            city="Curitiba",
            state="PR",
        )

        self.client.force_authenticate(self.user)

    def gift_data(self):
        return {
            "name": "Geladeira Frost Free",
            "description": "Geladeira Brastemp 400L",
            "price": "3599.90",
            "quantity": 1,
            "reserved": 0,
            "is_active": True,
        }

    def test_create_gift(self):
        url = reverse("gift-list")

        response = self.client.post(
            url,
            self.gift_data(),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            Gift.objects.count(),
            1,
        )

        self.assertEqual(
            Gift.objects.first().wedding,
            self.wedding,
        )

    def test_list_only_own_gifts(self):
        Gift.objects.create(
            wedding=self.wedding,
            **self.gift_data(),
        )

        Gift.objects.create(
            wedding=self.other_wedding,
            name="Fogão",
            description="Fogão 5 bocas",
            price="2500.00",
            quantity=1,
        )

        url = reverse("gift-list")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

    def test_update_gift(self):
        gift = Gift.objects.create(
            wedding=self.wedding,
            **self.gift_data(),
        )

        url = reverse(
            "gift-detail",
            args=[gift.id],
        )

        response = self.client.patch(
            url,
            {
                "price": "3999.90",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        gift.refresh_from_db()

        self.assertEqual(
            str(gift.price),
            "3999.90",
        )

    def test_delete_gift(self):
        gift = Gift.objects.create(
            wedding=self.wedding,
            **self.gift_data(),
        )

        url = reverse(
            "gift-detail",
            args=[gift.id],
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertEqual(
            Gift.objects.count(),
            0,
        )

    def test_search_gift(self):
        Gift.objects.create(
            wedding=self.wedding,
            **self.gift_data(),
        )

        url = reverse("gift-list")

        response = self.client.get(
            url,
            {
                "search": "Geladeira",
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

    def test_filter_reserved(self):
        data = self.gift_data()
        data["reserved"] = 2

        Gift.objects.create(
            wedding=self.wedding,
            **data,
        )

        url = reverse("gift-list")

        response = self.client.get(
            url,
            {
                "reserved": 2,
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

    def test_ordering_price(self):
        Gift.objects.create(
            wedding=self.wedding,
            name="TV",
            description="TV 55 Polegadas",
            price="5000.00",
            quantity=1,
        )

        Gift.objects.create(
            wedding=self.wedding,
            **self.gift_data(),
        )

        url = reverse("gift-list")

        response = self.client.get(
            url,
            {
                "ordering": "-price",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data[0]["name"],
            "TV",
        )
