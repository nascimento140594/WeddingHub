from django.urls import path

from .views import (
    PublicWeddingView,
    WeddingCreateView,
    WeddingDetailView,
)

app_name = "wedding"

urlpatterns = [
    path(
        "",
        WeddingCreateView.as_view(),
        name="create",
    ),
    path(
        "me/",
        WeddingDetailView.as_view(),
        name="detail",
    ),
    path(
        "public/<slug:slug>/",
        PublicWeddingView.as_view(),
        name="public",
    ),
]
