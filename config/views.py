"""Project-level pages: the public landing page and the logged-in home page."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from apps.ui_preview import fake_data


def landing(request):
    """The public front page at /. Logged-in visitors go straight to their home page."""
    if request.user.is_authenticated:
        return redirect("home")
    # Two example cards for the hero illustration (they aren't links).
    # Swap in real postings once the Posting model exists.
    context = {"sample_postings": fake_data.landing_postings()}
    return render(request, "pages/landing.html", context)


class HomeView(LoginRequiredMixin, TemplateView):
    """A placeholder until the home dashboard (#27) exists.

    The finished design is templates/pages/home.html; see docs/frontend-handoff.md.
    """

    template_name = "pages/home_placeholder.html"
