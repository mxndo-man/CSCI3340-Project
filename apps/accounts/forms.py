from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import CustomUser  # Grabs the custom user model thats in apps


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email Address")

    # django-types' stubs omit UserCreationForm.Meta and clean_username; Django has both.
    class Meta(UserCreationForm.Meta):  # pyright: ignore[reportAttributeAccessIssue]
        model = CustomUser
        fields = (
            "username",
            "email",
        )  # Reqiure usernmae and email when creating new user.

    def clean_username(self):
        username = super().clean_username()  # pyright: ignore[reportAttributeAccessIssue]
        if username and "@" in username:
            raise ValidationError("Usernames cannot contain the '@' symbol.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if email and CustomUser.objects.filter(email__iexact=email).exists():
            raise ValidationError("A user with that email address already exists.")

        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = ""


class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("display_name", "graduation_term", "time_zone")
