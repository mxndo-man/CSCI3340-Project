"""Project-level pages: the public landing page and the logged-in home page."""

from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.staticfiles import finders
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

# The landing page's hero art. Until this file exists, the page shows a flat stand-in.
HERO_IMAGE = "img/landing/hero-valley.webp"


def _samples():
    """Sample postings, reviews and boards for the landing page's small copies of the app.

    They come from the preview's fake data while that app is installed; without it the
    lists are empty and the page skips those blocks. Swap in real querysets (for example
    a few open postings) once the models exist.
    """
    if not apps.is_installed("apps.ui_preview"):
        return {"sample_postings": [], "sample_reviews": [], "sample_boards": []}
    from apps.ui_preview import fake_data  # only while the preview app exists

    world = fake_data.world()
    # Two postings that differ on clearance and deadline, so the chips show their range.
    postings = [world.postings[0], world.postings[2]]
    return {
        "sample_postings": postings,
        "sample_reviews": world.reviews_for(postings[0]) if postings else [],
        "sample_boards": world.my_boards()[:2],
    }


def landing(request):
    """The public front page at /. Logged-in visitors go straight to their home page."""
    if request.user.is_authenticated:
        return redirect("home")
    context = _samples()
    context["hero_image"] = HERO_IMAGE if finders.find(HERO_IMAGE) else ""
    return render(request, "pages/landing.html", context)


class HomeView(LoginRequiredMixin, TemplateView):
    """A placeholder until the home dashboard (#27) exists.

    The finished design is templates/pages/home.html; see docs/frontend-handoff.md.
    """

    template_name = "pages/home_placeholder.html"
