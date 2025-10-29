from django.contrib import admin
from .models import Rental


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "scooter",
        "start_time",
        "end_time",
    )
    list_filter = ("start_time", "end_time")
    search_fields = ("user__email", "scooter__name")
    ordering = ("-start_time",)
