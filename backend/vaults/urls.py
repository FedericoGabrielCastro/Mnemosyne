from django.urls import include, path
from rest_framework.routers import DefaultRouter

from vaults.views import VaultViewSet, health

router = DefaultRouter()
router.register("vaults", VaultViewSet, basename="vault")

urlpatterns = [
    path("health/", health),
    path("", include(router.urls)),
]
