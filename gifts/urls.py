from rest_framework.routers import DefaultRouter

from .views import GiftViewSet

router = DefaultRouter()
router.register("", GiftViewSet, basename="gift")

urlpatterns = router.urls
