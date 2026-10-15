from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, get_user_model
from .models import CustomUser  # Grabs the custom user model thats in apps

class CustomUserCreationForm(UserCreationForm):

    email = forms.EmailField(required=True, label="Email Address")

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email',) # Reqiure usernmae and email when creating new user.
    
        # Input validation, will later be fixed.

class CustomLoginForm(forms.Form):
    username_or_email = forms.CharField(
        label="Username or Email")

    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):

        cleaned_data = super().clean()  # Input Safety Validation
        identifier = cleaned_data.get("username_or_email")  # Grabs the "cleaned" username_or_email
        password = cleaned_data.get("password") # Grabs the "cleaned" password

        if identifier and password:
            self.user_cache = authenticate(
                username=identifier,
                password=password,
                backend='apps.accounts.backend.EmailOrUsernameModelBackend' # Back end that checks email/password for login
            )
            
            # If the backend returned None, it means authentication failed
            if self.user_cache is None:
                raise forms.ValidationError(
                    "Invalid username/email or password. Please try again."
                )