from django.urls import path
from . import views

app_name = "scooters"

urlpatterns = [
    path("", views.scooter_list, name="scooter-list"),
    path("scooter/<slug:slug>/", views.scooter_detail, name="scooter-detail"),
]
