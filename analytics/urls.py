from django.urls import path

from .views import (
    DashboardPageView,
    DashboardView,
)


urlpatterns = [
    path(
        "",
        DashboardView.as_view(),
        name="dashboard",
    ),
    path(
        "page/",
        DashboardPageView.as_view(),
        name="dashboard-page",
    ),
]
