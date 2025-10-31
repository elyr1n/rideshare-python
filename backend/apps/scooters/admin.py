from django.contrib import admin
from .models import ScooterModel, Scooter


@admin.register(ScooterModel)
class ScooterModelAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "city",
        "description",
    )
    list_filter = ("name", "city")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Scooter)
class ScooterAdmin(admin.ModelAdmin):
    list_display = (
        "slug",
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
    search_fields = ("slug",)
