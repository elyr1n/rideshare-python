from django.urls import path
from . import views

app_name = "scooters"

urlpatterns = [
    path("", views.scooter_models_list, name="scooter-models-list"),
    path("scooters/<slug:model_slug>/", views.scooter_list, name="scooter-list"),
    path("scooter/<slug:scooter_slug>/", views.scooter_detail, name="scooter-detail"),
]
