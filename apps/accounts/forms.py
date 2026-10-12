from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser  # Grabs the custom user model thats in apps

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email',)
        # Input validation, will later be fixed to prevent SQL Injections or something who knows