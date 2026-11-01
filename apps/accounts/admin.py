from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("username", "email", "usable_password", "password1", "password2")}),
    )
    fieldsets = (
        *UserAdmin.fieldsets,
        ("Profile", {"fields": ("display_name", "graduation_term", "time_zone")}),
    )