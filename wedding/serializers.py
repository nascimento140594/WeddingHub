from rest_framework import serializers

from .models import Wedding


class WeddingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wedding
        fields = "__all__"
        read_only_fields = (
            "id",
            "owner",
            "slug",
            "created_at",
            "updated_at",
        )
