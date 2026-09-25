from django import forms

from .models import Gift


class GiftForm(forms.ModelForm):
    class Meta:
        model = Gift
        fields = [
            "name",
            "description",
            "price",
            "image",
            "quantity",
            "reserved",
            "is_active",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Nome do presente",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Descrição do presente",
                }
            ),
            "price": forms.NumberInput(
                attrs={
                    "step": "0.01",
                    "min": "0",
                    "placeholder": "0,00",
                }
            ),
            "image": forms.ClearableFileInput(),
            "quantity": forms.NumberInput(
                attrs={
                    "min": 1,
                }
            ),
            "reserved": forms.NumberInput(
                attrs={
                    "min": 0,
                }
            ),
            "is_active": forms.CheckboxInput(),
        }
