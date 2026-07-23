from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Gift
from .serializers import GiftSerializer


class GiftViewSet(viewsets.ModelViewSet):
    serializer_class = GiftSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Gift.objects.filter(
            wedding__owner=self.request.user
        )

    def perform_create(self, serializer):
        wedding = self.request.user.wedding
        serializer.save(wedding=wedding)
