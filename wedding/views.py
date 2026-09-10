from django.shortcuts import get_object_or_404, render

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Wedding
from .serializers import WeddingSerializer


class WeddingCreateView(generics.CreateAPIView):
    serializer_class = WeddingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class WeddingDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = WeddingSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(
            Wedding,
            owner=self.request.user,
        )


class PublicWeddingView(generics.GenericAPIView):
    permission_classes = []

    def get(self, request, slug):
        wedding = get_object_or_404(
            Wedding,
            slug=slug,
            is_public=True,
        )

        return render(
            request,
            "wedding/public.html",
            {
                "wedding": wedding,
            },
        )
