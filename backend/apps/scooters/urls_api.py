from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_api import CityViewSet, ScooterModelViewSet, ScooterViewSet

router = DefaultRouter()
router.register(r"cities", CityViewSet, basename="city")
router.register(r"models", ScooterModelViewSet, basename="scooter-model")
router.register(r"scooters", ScooterViewSet, basename="scooter")

urlpatterns = [
    path("api/", include(router.urls)),
]
