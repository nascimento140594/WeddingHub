from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated

from .forms import GiftForm
from .models import Gift
from .serializers import GiftSerializer

from wedding.models import Wedding


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


@login_required
def gift_list_page(request):
    wedding = get_object_or_404(
        Wedding,
        owner=request.user,
    )

    gifts = Gift.objects.filter(
        wedding=wedding,
    ).order_by("name")

    return render(
        request,
        "gifts/gift_list.html",
        {
            "wedding": wedding,
            "gifts": gifts,
        },
    )


@login_required
def gift_create_page(request):
    wedding = get_object_or_404(
        Wedding,
        owner=request.user,
    )

    if request.method == "POST":
        form = GiftForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():
            gift = form.save(commit=False)
            gift.wedding = wedding
            gift.save()

            return redirect(
                "gifts:gift-page",
            )

    else:
        form = GiftForm()

    return render(
        request,
        "gifts/gift_form.html",
        {
            "wedding": wedding,
            "form": form,
            "title": "Novo presente",
        },
    )


@login_required
def gift_edit_page(request, pk):
    wedding = get_object_or_404(
        Wedding,
        owner=request.user,
    )

    gift = get_object_or_404(
        Gift,
        pk=pk,
        wedding=wedding,
    )

    if request.method == "POST":
        form = GiftForm(
            request.POST,
            request.FILES,
            instance=gift,
        )

        if form.is_valid():
            form.save()

            return redirect(
                "gifts:gift-page",
            )

    else:
        form = GiftForm(
            instance=gift,
        )

    return render(
        request,
        "gifts/gift_form.html",
        {
            "wedding": wedding,
            "form": form,
            "title": "Editar presente",
            "gift": gift,
        },
    )


@login_required
def gift_delete_page(request, pk):
    wedding = get_object_or_404(
        Wedding,
        owner=request.user,
    )

    gift = get_object_or_404(
        Gift,
        pk=pk,
        wedding=wedding,
    )

    if request.method == "POST":
        gift.delete()

        return redirect(
            "gifts:gift-page",
        )

    return render(
        request,
        "gifts/gift_delete.html",
        {
            "wedding": wedding,
            "gift": gift,
        },
    )
