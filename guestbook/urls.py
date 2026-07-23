from rest_framework.routers import DefaultRouter

from .views import GuestMessageViewSet

router = DefaultRouter()

router.register(
    "",
    GuestMessageViewSet,
    basename="guestbook",
)

urlpatterns = router.urls
