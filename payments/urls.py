from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import PaymentViewSet, mercadopago_webhook

router = DefaultRouter()
router.register("", PaymentViewSet, basename="payment")

urlpatterns = [
    path(
        "webhook/",
        mercadopago_webhook,
        name="mercadopago-webhook",
    ),
]

urlpatterns += router.urls
