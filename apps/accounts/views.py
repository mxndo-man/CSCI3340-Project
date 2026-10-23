# Create your views here.
# apps/accounts/views.py
from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST


def home_view(request):
    """Renders the public blank homepage."""
    return render(request, "../templates/base.html")


@require_POST
def logout_view(request):
    logout(request)
    return redirect("home")


def login_page(request):
    if (
        request.user.is_authenticated
    ):  # If user is already logged in, send them to home page
        return redirect("home")
    # Renders the login page that would be in apps/accounts/templates/...
    return render(request, "apps/accounts/templates/login_page.html")
