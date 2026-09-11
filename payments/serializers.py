from rest_framework import serializers

from gifts.models import Gift

from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = (
            "id",
            "created_at",
        )


class CheckoutSerializer(serializers.Serializer):
    gift = serializers.PrimaryKeyRelatedField(
        queryset=Gift.objects.filter(
            is_active=True,
            wedding__is_public=True,
        ),
    )
    guest_name = serializers.CharField(
        max_length=255,
    )
    guest_email = serializers.EmailField()

    def validate_gift(self, gift):
        if gift.reserved >= gift.quantity:
            raise serializers.ValidationError(
                "Este presente já foi reservado."
            )

        return gift
