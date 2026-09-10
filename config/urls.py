from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("admin/", admin.site.urls),

    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="registration/login.html",
        ),
        name="login",
    ),

    path(
        "api/accounts/",
        include("accounts.urls"),
    ),

    path(
        "api/wedding/",
        include("wedding.urls"),
    ),

    path(
        "api/guests/",
        include("guests.urls"),
    ),

    path(
        "api/gifts/",
        include("gifts.urls"),
    ),

    path(
        "api/payments/",
        include("payments.urls"),
    ),

    path(
        "api/guestbook/",
        include("guestbook.urls"),
    ),

    path(
        "api/dashboard/",
        include("analytics.urls"),
    ),

    path(
        "api/token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),

    path(
        "api/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),

    path(
        "api/schema/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),

    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(
            url_name="schema",
        ),
        name="swagger-ui",
    ),
]
