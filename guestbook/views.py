from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import GuestMessage
from .serializers import GuestMessageSerializer


class GuestMessageViewSet(viewsets.ModelViewSet):
    serializer_class = GuestMessageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    queryset = GuestMessage.objects.select_related("wedding")

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = [
        "approved",
    ]

    search_fields = [
        "guest_name",
        "guest_email",
        "message",
    ]

    ordering_fields = [
        "guest_name",
        "created_at",
    ]

    ordering = [
        "-created_at",
    ]

    def get_queryset(self):
        queryset = self.queryset

        if self.request.user.is_authenticated:
            return queryset.filter(
                wedding__owner=self.request.user,
            )

        return queryset.filter(
            approved=True,
        )
