from django.shortcuts import render
from django.views import View


class PaymentResultView(View):
    template_name = "payments/result.html"

    def get(self, request, result):
        titles = {
            "sucesso": "Pagamento aprovado",
            "pendente": "Pagamento pendente",
            "falhou": "Pagamento não aprovado",
        }

        messages = {
            "sucesso": "Obrigado pelo carinho! O presente foi registrado com sucesso.",
            "pendente": "Seu pagamento ainda está sendo processado. O status será atualizado automaticamente.",
            "falhou": "O pagamento não foi concluído. Você pode voltar à lista de presentes e tentar novamente.",
        }

        return render(
            request,
            self.template_name,
            {
                "title": titles.get(result, "Pagamento"),
                "message": messages.get(
                    result,
                    "Confira o status do seu pagamento.",
                ),
            },
        )
