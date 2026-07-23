from django.contrib import admin
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
    # Admin
    path(
        "admin/",
        admin.site.urls,
    ),

    # Accounts
    path(
        "api/accounts/",
        include("accounts.urls"),
    ),

    # Wedding
    path(
        "api/wedding/",
        include("wedding.urls"),
    ),

    # Guests
    path(
        "api/guests/",
        include("guests.urls"),
    ),

    # Gifts
    path(
        "api/gifts/",
        include("gifts.urls"),
    ),

    # Payments
    path(
        "api/payments/",
        include("payments.urls"),
    ),

    # Guestbook
    path(
        "api/guestbook/",
        include("guestbook.urls"),
    ),

    # Dashboard / Analytics
    path(
        "api/dashboard/",
        include("analytics.urls"),
    ),

    # JWT Authentication
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

    # API Documentation
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
