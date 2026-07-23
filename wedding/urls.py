from django.urls import path

from .views import (
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
]
