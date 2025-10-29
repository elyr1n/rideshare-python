from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "first_name",
        "last_name",
        "phone_number",
        "is_driver",
        "balance",
    )
    list_filter = (
        "is_driver",
        "is_staff",
        "is_superuser",
    )
    search_fields = (
        "email",
        "first_name",
        "last_name",
        "phone_number",
    )
    ordering = ("email",)
