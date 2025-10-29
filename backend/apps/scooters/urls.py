from django.urls import path
from . import views

app_name = "scooters"

urlpatterns = [
    path("", views.scooter_list, name="scooter-list"),
]
