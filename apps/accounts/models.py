import zoneinfo

from django.contrib.auth.models import AbstractUser
from django.db import models


def get_timezone_choices():
    return [(tz, tz) for tz in sorted(zoneinfo.available_timezones())]

class CustomUser(AbstractUser):
    # Make emails unique and required
    email = models.EmailField(
        unique=True, blank=False, verbose_name="Email Address"
    )  # Email for admins, eye
    username = models.CharField(max_length=30, unique=True)

    Grad_Terms = (
        ("Spring 2027", "Spring 2027"),
        ("Summer 2027", "Summer 2027"),
        ("Fall 2027", "Fall 2027"),
        ("Spring 2028", "Spring 2028"),
        ("Summer 2028", "Summer 2028"),
        ("Fall 2028", "Fall 2028"),
    )

    # Timezones = [(tz, tz) for tz in sorted(zoneinfo.available_timezones())]

    display_name = models.CharField(max_length=100, blank=True)
    graduation_term = models.CharField(max_length=20, choices=Grad_Terms, blank=True)
    # time_zone = models.CharField(
    #     max_length=100,
    #     choices=Timezones,
    #     default="UTC",
    #     help_text="Select your local timezone.",
    # )
    time_zone = models.CharField(
        max_length=100, default="UT", help_text="Select your local timezone.", choices=get_timezone_choices,
    )
    # Timezones might require middleware setup for dynamic calls, but for now its being left like this

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"] # noqa: RUF012
    # me:1 , ruff:0

    def __str__(self):
        return self.email
