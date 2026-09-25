from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import (
    GiftViewSet,
    gift_create_page,
    gift_delete_page,
    gift_edit_page,
    gift_list_page,
)


app_name = "gifts"


router = DefaultRouter()

router.register(
    "",
    GiftViewSet,
    basename="gift",
)


urlpatterns = [
    path(
        "page/",
        gift_list_page,
        name="gift-page",
    ),

    path(
        "new/",
        gift_create_page,
        name="gift-create",
    ),

    path(
        "<int:pk>/edit/",
        gift_edit_page,
        name="gift-edit",
    ),

    path(
        "<int:pk>/delete/",
        gift_delete_page,
        name="gift-delete",
    ),
]


urlpatterns += router.urls
