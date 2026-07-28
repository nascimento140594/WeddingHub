from django.utils import timezone

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Guest
from .serializers import GuestSerializer


class GuestViewSet(viewsets.ModelViewSet):
    serializer_class = GuestSerializer
    permission_classes = [IsAuthenticated]

    queryset = Guest.objects.select_related("wedding")

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = [
        "status",
    ]

    search_fields = [
        "full_name",
        "email",
        "phone",
    ]

    ordering_fields = [
        "full_name",
        "created_at",
        "status",
    ]

    ordering = [
        "full_name",
    ]

    def get_queryset(self):
        return self.queryset.filter(
            wedding__owner=self.request.user,
        )

    def perform_create(self, serializer):
        serializer.save(
            wedding=self.request.user.wedding,
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="confirm",
    )
    def confirm(self, request, pk=None):
        guest = self.get_object()

        guest.status = Guest.Status.CONFIRMED
        guest.confirmed_at = timezone.now()
        guest.companions = request.data.get(
            "companions",
            guest.companions,
        )
        guest.message = request.data.get(
            "message",
            "",
        )
        guest.save()

        return Response(
            GuestSerializer(guest).data,
            status=status.HTTP_200_OK,
        )

    @action(
        detail=True,
        methods=["post"],
        url_path="decline",
    )
    def decline(self, request, pk=None):
        guest = self.get_object()

        guest.status = Guest.Status.DECLINED
        guest.confirmed_at = None
        guest.save()

        return Response(
            GuestSerializer(guest).data,
            status=status.HTTP_200_OK,
        )
