from rest_framework import serializers

from .models import GuestMessage


class GuestMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuestMessage
        fields = "__all__"
        read_only_fields = (
            "id",
            "created_at",
            "approved",
        )
