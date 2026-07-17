from django.urls import path

from .views import (
    MeView,
    RegisterUserView,
)

app_name = "accounts"

urlpatterns = [
    path(
        "register/",
        RegisterUserView.as_view(),
        name="register",
    ),
    path(
        "me/",
        MeView.as_view(),
        name="me",
    ),
]
