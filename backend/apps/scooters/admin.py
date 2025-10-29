from django.contrib import admin
from .models import Scooter


@admin.register(Scooter)
class ScooterAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "latitude",
        "longitude",
        "battery_level",
        "is_available",
    )
    list_filter = ("is_available", "battery_level")
    search_fields = ("id", "name")
    ordering = ("id",)
