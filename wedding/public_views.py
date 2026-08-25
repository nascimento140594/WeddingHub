from django.shortcuts import get_object_or_404, render
from django.views import View

from gifts.models import Gift

from .models import Wedding


class PublicWeddingView(View):
    template_name = "wedding/public.html"

    def get(self, request, slug):
        wedding = get_object_or_404(
            Wedding.objects.prefetch_related("gifts"),
            slug=slug,
            is_public=True,
        )

        gifts = Gift.objects.filter(
            wedding=wedding,
            is_active=True,
        ).order_by("name")

        return render(
            request,
            self.template_name,
            {
                "wedding": wedding,
                "gifts": gifts,
            },
        )
