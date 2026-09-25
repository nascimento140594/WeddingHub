from django import forms

from .models import Guest


class GuestForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = [
            "full_name",
            "email",
            "phone",
            "invitation_code",
            "companions",
            "status",
            "notes",
        ]

        widgets = {
            "full_name": forms.TextInput(
                attrs={
                    "placeholder": "Nome completo",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "E-mail",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "placeholder": "Telefone",
                }
            ),
            "invitation_code": forms.TextInput(
                attrs={
                    "placeholder": "Código do convite",
                }
            ),
            "companions": forms.NumberInput(
                attrs={
                    "min": 0,
                }
            ),
            "status": forms.Select(),
            "notes": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Observações",
                }
            ),
        }
