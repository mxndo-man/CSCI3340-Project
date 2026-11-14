import zoneinfo

from django.contrib.auth.models import AbstractUser
from django.db import models


def get_timezone_choices():
    return [(tz, tz) for tz in sorted(zoneinfo.available_timezones())]


class CustomUser(AbstractUser):
    # Make emails unique and required
    email = models.EmailField(
        unique=True, verbose_name="Email Address"
    )  # Email for admins, eye

    Grad_Terms = (
        ("Spring 2027", "Spring 2027"),
        ("Summer 2027", "Summer 2027"),
        ("Fall 2027", "Fall 2027"),
        ("Spring 2028", "Spring 2028"),
        ("Summer 2028", "Summer 2028"),
        ("Fall 2028", "Fall 2028"),
    )

    display_name = models.CharField(max_length=100, blank=True)
    graduation_term = models.CharField(max_length=20, choices=Grad_Terms, blank=True)

    time_zone = models.CharField(
        max_length=100,
        default="America/Chicago",
        help_text="Select your local timezone.",
        # Django 5+ accepts a callable here; django-types' stubs don't know that yet.
        choices=get_timezone_choices,  # pyright: ignore[reportArgumentType]
    )
    # Timezones might require middleware setup for dynamic calls, but for now its being left like this

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]  # noqa: RUF012
    # me:1 , ruff:0

    def __str__(self):
        return self.username
