from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import (
    GuestViewSet,
    guest_list_page,
    public_rsvp,
)


router = DefaultRouter()

router.register(
    "",
    GuestViewSet,
    basename="guest",
)


urlpatterns = [
    path(
        "page/",
        guest_list_page,
        name="guest-page",
    ),

    path(
        "rsvp/<slug:slug>/",
        public_rsvp,
        name="public-rsvp",
    ),
]

urlpatterns += router.urls
