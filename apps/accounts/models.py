import zoneinfo

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    # Make emails unique and required
    email = models.EmailField(
        unique=True, blank=True, verbose_name="Email Address"
    )  # Allows email to be blank for admins, but will require it forms.py
    username = models.CharField(max_length=30, unique=True)

    Grad_Terms = [
        ("SP27", "Spring 2027"),
        ("SU27", "Summer 2027"),
        ("FA27", "Fall 2027"),
        ("SP28", "Spring 2028"),
        ("SU28", "Summer 2028"),
        ("FA28", "Fall 2028"),
    ]

    Timezones = [(tz, tz) for tz in sorted(zoneinfo.available_timezones())]

    display_name = models.CharField(max_length=50, blank=True)
    graduation_term = models.CharField(max_length=4, choices=Grad_Terms, blank=True)
    time_zone = models.CharField(
        max_length=100,
        choices=Timezones,
        default="UTC",
        help_text="Select your local timezone.",
    )
    # Timezones might require middleware setup for dynamic calls, but for now its being left like this

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
