from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from apps.accounts.forms import CustomUserCreationForm

def real_home_view(request):
    """Renders the public blank homepage."""
    return render(request, '../templates/base.html')