"""Project-level pages: the public landing page and the logged-in home page."""

from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import TemplateView


def _sample_postings():
    """Two example cards for the hero illustration (they aren't links).

    They come from the preview's fake data while that app is installed, and the hero simply
    has no cards without it. Swap in real postings once the Posting model exists.
    """
    if not apps.is_installed("apps.ui_preview"):
        return []
    from apps.ui_preview import fake_data  # only while the preview app exists

    return fake_data.landing_postings()


def landing(request):
    """The public front page at /. Logged-in visitors go straight to their home page."""
    if request.user.is_authenticated:
        return redirect("home")
    return render(
        request, "pages/landing.html", {"sample_postings": _sample_postings()}
    )


class HomeView(LoginRequiredMixin, TemplateView):
    """A placeholder until the home dashboard (#27) exists.

    The finished design is templates/pages/home.html; see docs/frontend-handoff.md.
    """

    template_name = "pages/home_placeholder.html"
