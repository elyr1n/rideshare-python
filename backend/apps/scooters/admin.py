from django.contrib import admin
from .models import Scooter


@admin.register(Scooter)
class ScooterAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "latitude",
        "longitude",
        "max_speed",
        "battery_level",
        "total_price",
        "is_available",
    )
    list_filter = (
        "is_available",
        "battery_level",
        "max_speed",
    )
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
