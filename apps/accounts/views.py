# Create your views here.
# apps/accounts/views.py
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import CustomUserCreationForm


def home_view(request):
    """Renders the public blank homepage."""
    return render(request, "accounts/index.html")


def register_view(request):
    """Handles displaying and processing the sign-up form."""
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Instantly sign them into their session
            return redirect("test_page")  # Redirect them behind the wall
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/register.html", {"form": form})


@login_required(login_url="/accounts/register/")
def test_page_view(request):
    """A blank test page locked behind an active user session authentication wall."""
    return render(request, "accounts/test_page.html")


def logout_view(request):
    """Logs out the user and sends them back home."""
    logout(request)
    return redirect("home")
