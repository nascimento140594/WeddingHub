from django.urls import path

from .public_views import PublicWeddingView

urlpatterns = [
    path(
        "<slug:slug>/",
        PublicWeddingView.as_view(),
        name="public-wedding",
    ),
]
