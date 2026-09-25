from django.db.models import F
from django.shortcuts import get_object_or_404, render

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Wedding
from .serializers import WeddingSerializer

from gifts.models import Gift


class WeddingCreateView(generics.CreateAPIView):
    serializer_class = WeddingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class WeddingDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = WeddingSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(
            Wedding,
            owner=self.request.user,
        )


class PublicWeddingView(generics.GenericAPIView):
    permission_classes = []

    def get(self, request, slug):
        wedding = get_object_or_404(
            Wedding,
            slug=slug,
            is_public=True,
        )

        gifts = Gift.objects.filter(
            wedding=wedding,
            is_active=True,
            reserved__lt=F("quantity"),
        ).order_by("id")

        home_gifts = []
        big_gifts = []
        honeymoon_gifts = []
        fun_gifts = []

        # ==================================================
        # IMAGENS
        # ==================================================

        home_image = (
            "https://images.pexels.com/photos/"
            "1599791/pexels-photo-1599791.jpeg"
        )

        big_image = (
            "https://images.pexels.com/photos/"
            "5824883/pexels-photo-5824883.jpeg"
        )

        honeymoon_image = (
            "https://images.pexels.com/photos/"
            "1024960/pexels-photo-1024960.jpeg"
        )

        fun_image = (
            "https://images.pexels.com/photos/"
            "3768916/pexels-photo-3768916.jpeg"
        )

        # ==================================================
        # CLASSIFICAÇÃO
        # ==================================================

        for gift in gifts:

            name = gift.name.lower()

            # ==================================================
            # NOSSO LAR
            # ==================================================

            if any(
                item in name
                for item in [
                    "jogo de panelas",
                    "air fryer",
                    "cafeteira",
                    "liquidificador",
                    "sanduicheira",
                    "panela de pressão",
                    "panela elétrica de arroz",
                    "grill elétrico",
                    "torradeira",
                    "aspirador",
                    "jogo de jantar",
                    "faqueiro",
                    "jogo de taças",
                    "jogo de cama",
                    "jogo de toalhas",
                    "edredom",
                ]
            ):

                gift.image_url = home_image

                home_gifts.append(gift)

            # ==================================================
            # GRANDES SONHOS PARA A CASA
            # ==================================================

            elif any(
                item in name
                for item in [
                    "geladeira",
                    "máquina de lavar",
                    "smart tv",
                ]
            ):

                gift.image_url = big_image

                big_gifts.append(gift)

            # ==================================================
            # LUA DE MEL
            # ==================================================

            elif any(
                item in name
                for item in [
                    "jantar romântico",
                    "diária da lua de mel",
                    "passeio romântico",
                    "spa para dois",
                    "café da manhã dos recém-casados",
                    "ensaio fotográfico na lua de mel",
                    "passeio especial dos noivos",
                ]
            ):

                gift.image_url = honeymoon_image

                honeymoon_gifts.append(gift)

            # ==================================================
            # MOMENTOS DOS RECÉM-CASADOS
            # ==================================================

            elif any(
                item in name
                for item in [
                    "noite da pizza",
                    "noite de filmes",
                    "vale delivery",
                    "date dos recém-casados",
                    "domingo preguiçoso",
                    "noite romântica",
                    "fundo vida de casados",
                ]
            ):

                gift.image_url = fun_image

                fun_gifts.append(gift)

            # ==================================================
            # SEGURANÇA
            # ==================================================

            else:

                gift.image_url = home_image

                home_gifts.append(gift)

        return render(
            request,
            "wedding/public.html",
            {
                "wedding": wedding,
                "gifts": gifts,
                "home_gifts": home_gifts,
                "big_gifts": big_gifts,
                "honeymoon_gifts": honeymoon_gifts,
                "fun_gifts": fun_gifts,
            },
        )
