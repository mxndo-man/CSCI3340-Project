from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    
    # Dont require a username
    username = None
    
    # Make emails unique and required
    email = models.EmailField(unique=True, verbose_name="Email Address")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email    