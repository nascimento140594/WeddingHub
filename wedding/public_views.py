from django.db.models import F
from django.shortcuts import get_object_or_404, render
from django.views import View

from gifts.models import Gift

from .models import Wedding


class PublicWeddingView(View):
    template_name = "wedding/public.html"

    def get(self, request, slug):
        wedding = get_object_or_404(
            Wedding.objects.prefetch_related("gifts"),
            slug=slug,
            is_public=True,
        )

        gifts = list(
            Gift.objects.filter(
                wedding=wedding,
                is_active=True,
                reserved__lt=F("quantity"),
            ).order_by("id")
        )

        home_gifts = []
        big_gifts = []
        honeymoon_gifts = []
        fun_gifts = []

        # ==================================================
        # IMAGENS DOS PRESENTES
        # ==================================================

        gift_images = {

            # --------------------------------------------------
            # NOSSO LAR
            # --------------------------------------------------

            "Jogo de Panelas":
                "https://images.unsplash.com/photo-1556911220-e15b29be8c8f"
                "?auto=format&fit=crop&w=900&q=85",

            "Air Fryer":
                "https://images.unsplash.com/photo-1556910103-1c02745aae4d"
                "?auto=format&fit=crop&w=900&q=85",

            "Cafeteira":
                "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085"
                "?auto=format&fit=crop&w=900&q=85",

            "Liquidificador":
                "https://images.unsplash.com/photo-1556911220-e15b29be8c8f"
                "?auto=format&fit=crop&w=900&q=85",

            "Sanduicheira":
                "https://images.unsplash.com/photo-1556910103-1c02745aae4d"
                "?auto=format&fit=crop&w=900&q=85",

            "Panela de Pressão Elétrica":
                "https://images.unsplash.com/photo-1556911220-e15b29be8c8f"
                "?auto=format&fit=crop&w=900&q=85",

            "Panela Elétrica de Arroz":
                "https://images.unsplash.com/photo-1556911220-e15b29be8c8f"
                "?auto=format&fit=crop&w=900&q=85",

            "Grill Elétrico":
                "https://images.unsplash.com/photo-1556910103-1c02745aae4d"
                "?auto=format&fit=crop&w=900&q=85",

            "Torradeira":
                "https://images.unsplash.com/photo-1556910103-1c02745aae4d"
                "?auto=format&fit=crop&w=900&q=85",

            "Aspirador de Pó":
                "https://images.unsplash.com/photo-1581578731548-c64695cc6952"
                "?auto=format&fit=crop&w=900&q=85",

            "Jogo de Jantar":
                "https://images.unsplash.com/photo-1519167758481-83f550bb49b3"
                "?auto=format&fit=crop&w=900&q=85",

            "Faqueiro":
                "https://images.unsplash.com/photo-1519167758481-83f550bb49b3"
                "?auto=format&fit=crop&w=900&q=85",

            "Jogo de Taças":
                "https://images.unsplash.com/photo-1519167758481-83f550bb49b3"
                "?auto=format&fit=crop&w=900&q=85",

            "Jogo de Cama":
                "https://images.unsplash.com/photo-1540518614846-7eded433c457"
                "?auto=format&fit=crop&w=900&q=85",

            "Jogo de Toalhas":
                "https://images.unsplash.com/photo-1600566753086-00f18fb6b3ea"
                "?auto=format&fit=crop&w=900&q=85",

            "Edredom do Casal":
                "https://images.unsplash.com/photo-1540518614846-7eded433c457"
                "?auto=format&fit=crop&w=900&q=85",

            # --------------------------------------------------
            # GRANDES SONHOS
            # --------------------------------------------------

            "Cota para a Geladeira - R$ 100":
                "https://images.unsplash.com/photo-1571175443880-49e1d25b2bc5"
                "?auto=format&fit=crop&w=900&q=85",

            "Cota para a Geladeira - R$ 200":
                "https://images.unsplash.com/photo-1571175443880-49e1d25b2bc5"
                "?auto=format&fit=crop&w=900&q=85",

            "Cota para a Geladeira - R$ 500":
                "https://images.unsplash.com/photo-1571175443880-49e1d25b2bc5"
                "?auto=format&fit=crop&w=900&q=85",

            "Cota para a Máquina de Lavar - R$ 100":
                "https://images.unsplash.com/photo-1626806787461-102c1bfaaea1"
                "?auto=format&fit=crop&w=900&q=85",

            "Cota para a Máquina de Lavar - R$ 200":
                "https://images.unsplash.com/photo-1626806787461-102c1bfaaea1"
                "?auto=format&fit=crop&w=900&q=85",

            "Cota para a Smart TV - R$ 250":
                "https://images.unsplash.com/photo-1593359677879-a4bb92f829d1"
                "?auto=format&fit=crop&w=900&q=85",

            "Cota para a Smart TV - R$ 500":
                "https://images.unsplash.com/photo-1593359677879-a4bb92f829d1"
                "?auto=format&fit=crop&w=900&q=85",

            # --------------------------------------------------
            # LUA DE MEL
            # --------------------------------------------------

            "Jantar Romântico":
                "https://images.unsplash.com/photo-1519167758481-83f550bb49b3"
                "?auto=format&fit=crop&w=900&q=85",

            "Uma Diária da Lua de Mel":
                "https://images.unsplash.com/photo-1566073771259-6a8506099945"
                "?auto=format&fit=crop&w=900&q=85",

            "Passeio Romântico":
                "https://images.unsplash.com/photo-1507525428034-b723cf961d3e"
                "?auto=format&fit=crop&w=900&q=85",

            "Spa para Dois":
                "https://images.unsplash.com/photo-1544161515-4ab6ce6db874"
                "?auto=format&fit=crop&w=900&q=85",

            "Café da Manhã dos Recém-Casados":
                "https://images.unsplash.com/photo-1523413651479-597eb2da0ad6"
                "?auto=format&fit=crop&w=900&q=85",

            "Ensaio Fotográfico na Lua de Mel":
                "https://images.unsplash.com/photo-1520854221256-17451cc331bf"
                "?auto=format&fit=crop&w=900&q=85",

            "Passeio Especial dos Noivos":
                "https://images.unsplash.com/photo-1526772662000-3f88f10405ff"
                "?auto=format&fit=crop&w=900&q=85",

            # --------------------------------------------------
            # MOMENTOS DOS RECÉM-CASADOS
            # --------------------------------------------------

            "Noite da Pizza":
                "https://images.unsplash.com/photo-1513104890138-7c749659a591"
                "?auto=format&fit=crop&w=900&q=85",

            "Noite de Filmes":
                "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba"
                "?auto=format&fit=crop&w=900&q=85",

            "Vale Delivery":
                "https://images.unsplash.com/photo-1504674900247-0877df9cc836"
                "?auto=format&fit=crop&w=900&q=85",

            "Date dos Recém-Casados":
                "https://images.unsplash.com/photo-1516589178581-6cd7833ae3b2"
                "?auto=format&fit=crop&w=900&q=85",

            "Domingo Preguiçoso":
                "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85"
                "?auto=format&fit=crop&w=900&q=85",

            "Noite Romântica":
                "https://images.unsplash.com/photo-1518199266791-5375a83190b7"
                "?auto=format&fit=crop&w=900&q=85",

            "Fundo Vida de Casados":
                "https://images.unsplash.com/photo-1524758631624-e2822e304c36"
                "?auto=format&fit=crop&w=900&q=85",

            "Vale Quem Manda na Casa?":
                "https://images.unsplash.com/photo-1516321497487-e288fb19713f"
                "?auto=format&fit=crop&w=900&q=85",
        }

        # ==================================================
        # CLASSIFICAÇÃO
        # ==================================================

        for gift in gifts:

            name = gift.name.strip()

            name_lower = name.lower()

            # Foto específica
            gift.image_url = gift_images.get(
                name,
                "https://images.unsplash.com/photo-1519741497674-611481863552"
                "?auto=format&fit=crop&w=900&q=85",
            )

            # ==================================================
            # NOSSO LAR
            # ==================================================

            if any(
                keyword in name_lower
                for keyword in [
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

                home_gifts.append(gift)

            # ==================================================
            # GRANDES SONHOS
            # ==================================================

            elif any(
                keyword in name_lower
                for keyword in [
                    "geladeira",
                    "máquina de lavar",
                    "maquina de lavar",
                    "smart tv",
                ]
            ):

                big_gifts.append(gift)

            # ==================================================
            # LUA DE MEL
            # ==================================================

            elif any(
                keyword in name_lower
                for keyword in [
                    "jantar romântico",
                    "jantar romantico",
                    "diária da lua de mel",
                    "diaria da lua de mel",
                    "passeio romântico",
                    "passeio romantico",
                    "spa para dois",
                    "café da manhã dos recém-casados",
                    "cafe da manha dos recem-casados",
                    "ensaio fotográfico na lua de mel",
                    "ensaio fotografico na lua de mel",
                    "passeio especial dos noivos",
                ]
            ):

                honeymoon_gifts.append(gift)

            # ==================================================
            # MOMENTOS
            # ==================================================

            elif any(
                keyword in name_lower
                for keyword in [
                    "noite da pizza",
                    "noite de filmes",
                    "vale delivery",
                    "date dos recém-casados",
                    "date dos recem-casados",
                    "domingo preguiçoso",
                    "domingo preguicoso",
                    "noite romântica",
                    "noite romantica",
                    "fundo vida de casados",
                    "quem manda na casa",
                ]
            ):

                fun_gifts.append(gift)

            else:

                home_gifts.append(gift)

        return render(
            request,
            self.template_name,
            {
                "wedding": wedding,
                "gifts": gifts,
                "home_gifts": home_gifts,
                "big_gifts": big_gifts,
                "honeymoon_gifts": honeymoon_gifts,
                "fun_gifts": fun_gifts,
            },
        )
