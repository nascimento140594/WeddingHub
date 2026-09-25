from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import (
    GuestViewSet,
    guest_create_page,
    guest_delete_page,
    guest_edit_page,
    guest_list_page,
    public_rsvp,
)


app_name = "guests"


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
        "new/",
        guest_create_page,
        name="guest-create",
    ),

    path(
        "<int:pk>/edit/",
        guest_edit_page,
        name="guest-edit",
    ),

    path(
        "<int:pk>/delete/",
        guest_delete_page,
        name="guest-delete",
    ),

    path(
        "rsvp/<slug:slug>/",
        public_rsvp,
        name="public-rsvp",
    ),
]


urlpatterns += router.urls
