from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Guest
from .serializers import GuestSerializer

from wedding.models import Wedding


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


@login_required
def guest_list_page(request):
    wedding = get_object_or_404(
        Wedding,
        owner=request.user,
    )

    guests = Guest.objects.filter(
        wedding=wedding,
    ).order_by("full_name")

    return render(
        request,
        "guests/guest_list.html",
        {
            "wedding": wedding,
            "guests": guests,
        },
    )


def public_rsvp(request, slug):

    wedding = get_object_or_404(
        Wedding,
        slug=slug,
        is_public=True,
    )

    invitation_code = request.GET.get(
        "convite",
        "",
    ).strip()

    guest = None

    if invitation_code:
        guest = Guest.objects.filter(
            wedding=wedding,
            invitation_code=invitation_code,
        ).first()

    if request.method == "POST":

        invitation_code = request.POST.get(
            "invitation_code",
            "",
        ).strip()

        guest = get_object_or_404(
            Guest,
            wedding=wedding,
            invitation_code=invitation_code,
        )

        guest.full_name = request.POST.get(
            "full_name",
            guest.full_name,
        ).strip()

        guest.email = request.POST.get(
            "email",
            guest.email,
        ).strip()

        guest.phone = request.POST.get(
            "phone",
            "",
        ).strip()

        guest.companions = int(
            request.POST.get(
                "companions",
                0,
            )
            or 0
        )

        guest.message = request.POST.get(
            "message",
            "",
        ).strip()

        response = request.POST.get(
            "response",
        )

        if response == "confirmed":

            guest.status = Guest.Status.CONFIRMED
            guest.confirmed_at = timezone.now()

        elif response == "declined":

            guest.status = Guest.Status.DECLINED
            guest.confirmed_at = None

        guest.save()

        return render(
            request,
            "guests/rsvp_success.html",
            {
                "wedding": wedding,
                "guest": guest,
            },
        )

    return render(
        request,
        "guests/rsvp.html",
        {
            "wedding": wedding,
            "guest": guest,
            "invitation_code": invitation_code,
        },
    )
