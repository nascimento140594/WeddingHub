from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated

from .models import Gift
from .serializers import GiftSerializer


class GiftViewSet(viewsets.ModelViewSet):
    serializer_class = GiftSerializer
    permission_classes = [IsAuthenticated]

    queryset = Gift.objects.select_related("wedding")

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = [
        "reserved",
    ]

    search_fields = [
        "name",
        "description",
    ]

    ordering_fields = [
        "name",
        "price",
        "created_at",
    ]

    ordering = [
        "name",
    ]

    def get_queryset(self):
        return self.queryset.filter(
            wedding__owner=self.request.user,
        )

    def perform_create(self, serializer):
        serializer.save(
            wedding=self.request.user.wedding,
        )
