from rest_framework import serializers

from .models import Guest


class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = "__all__"
        read_only_fields = (
            "id",
            "created_at",
            "wedding",
            "confirmed_at",
        )
