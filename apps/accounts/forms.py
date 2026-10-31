from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import CustomUser  # Grabs the custom user model thats in apps


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email Address")

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = (
            "username",
            "email",
        )  # Reqiure usernmae and email when creating new user.

    def clean_username(self):
        username = self.cleaned_data.get("username")

        if username and "@" in username:
            raise ValidationError("Usernames cannot contain the '@' symbol.")

        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if email and CustomUser.objects.filter(email__iexact=email).exists():
            raise ValidationError("A user with that email address already exists.")

        return email


class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("display_name", "graduation_term", "time_zone")
