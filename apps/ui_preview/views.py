"""The style guide (every UI component on one page) and the preview pages.

Preview pages render the real templates with fake objects from fake_data.py, so the UI
works before the models exist. Nothing here touches the database.
"""

from datetime import timedelta
from pathlib import Path
from types import SimpleNamespace

from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import AnonymousUser
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from . import fake_data
from .filters import SORTS, filter_postings, parse_filters


class StyleguideForm(forms.Form):
    """A form with one of each input, so the style guide can show fields and their errors."""

    name = forms.CharField(
        label="Board name", help_text="Everyone on the board sees it."
    )
    email = forms.EmailField(label="Email")
    term = forms.ChoiceField(
        label="Graduation term",
        choices=[
            ("", "Choose a term"),
            ("Fall 2027", "Fall 2027"),
            ("Spring 2028", "Spring 2028"),
        ],
        required=False,
    )
    notes = forms.CharField(
        label="Notes", widget=forms.Textarea(attrs={"rows": 3}), required=False
    )
    digest = forms.BooleanField(label="Email me a daily digest", required=False)


def styleguide(request):
    """Every component, for copying markup. Served at /styleguide/ only when DEBUG is on."""
    today = timezone.localdate()
    invalid = StyleguideForm({"name": "", "email": "not-an-email"})
    invalid.is_valid()  # fills in the errors, so the error state shows
    people = [
        SimpleNamespace(id=1, display_name="Liam R.", username="liamr"),
        SimpleNamespace(id=2, display_name="Maya K.", username="mayak"),
        SimpleNamespace(id=3, display_name="Arjun P.", username="arjunp"),
        SimpleNamespace(id=4, display_name="", username="jordans"),
    ]
    icon_dir = Path(settings.BASE_DIR) / "templates" / "components" / "icons"
    context = {
        "form": StyleguideForm(),
        "invalid_form": invalid,
        "people": people,
        "deadlines": [today + timedelta(days=n) for n in (0, 3, 8, 21, -2)],
        "icons": sorted(path.stem for path in icon_dir.glob("*.html")),
    }
    return render(request, "ui_preview/styleguide.html", context)


# ---- Preview pages ----------------------------------------------------------------------

# Every form the templates post. Real views pass `form_urls` with their own URLs; the
# preview sends them all to `action`. docs/frontend-handoff.md lists each form's fields.
FORM_ACTIONS = (
    "save_to_board",
    "remove_from_board",
    "track",
    "review_field",
    "add_posting",
    "save_search",
    "create_board",
    "join_board",
    "comment",
    "move_application",
    "add_task",
    "toggle_task",
    "toggle_alerts",
    "delete_saved_search",
    "update_preferences",
    "mark_all_read",
)


def _context(request, world, nav_active="", **extra):
    """What every preview page gets. ?as=visitor shows the logged-out version."""
    visitor = request.GET.get("as") == "visitor"
    action_url = reverse("ui_preview:action")
    context = {
        "ui_preview": True,
        "nav_active": nav_active,
        "user": AnonymousUser() if visitor else world.me,
        "form_urls": dict.fromkeys(FORM_ACTIONS, action_url),
        "my_boards": [] if visitor else world.my_boards(),
    }
    context.update(extra)
    return context


@require_POST
def action(request):
    """Every preview form posts here. Nothing is saved; it says so and goes back."""
    messages.info(request, "Preview only, nothing was saved")
    target = request.POST.get("next") or request.META.get("HTTP_REFERER", "")
    safe = url_has_allowed_host_and_scheme(
        target, allowed_hosts={request.get_host()}, require_https=request.is_secure()
    )
    return redirect(target if safe else reverse("ui_preview:index"))


def index(request):
    """A list of every preview page."""
    world = fake_data.world()
    pages = [
        ("Discover", reverse("ui_preview:discover"), "postings/discover.html"),
        (
            "A posting with a fact to check",
            reverse("ui_preview:posting_detail", args=[1]),
            "postings/detail.html",
        ),
        (
            "A posting with two facts to check",
            reverse("ui_preview:posting_detail", args=[8]),
            "postings/detail.html",
        ),
        (
            "A closed posting",
            reverse("ui_preview:posting_detail", args=[12]),
            "postings/detail.html",
        ),
        ("Add a posting", reverse("ui_preview:posting_add"), "postings/add.html"),
    ]
    return render(
        request, "ui_preview/index.html", _context(request, world, pages=pages)
    )


def discover(request):
    world = fake_data.world()
    filters = parse_filters(request.GET)
    sort = request.GET.get("sort", "closing")
    if sort not in SORTS:
        sort = "closing"
    results = filter_postings(world.postings, filters, world.today, sort)
    open_postings = [p for p in world.postings if p.status == "OPEN"]
    context = _context(
        request,
        world,
        "postings",
        page_obj=Paginator(results, 6).get_page(request.GET.get("page")),
        filters=filters,
        sort=sort,
        start_terms=sorted({p.start_term for p in open_postings if p.start_term}),
        total_count=len(open_postings),
        employer_count=len({p.organization for p in open_postings}),
        last_synced_at=world.now - timedelta(hours=2),
        search_saved=world.has_saved_search(filters),
    )
    return render(request, "postings/discover.html", context)


def posting_detail(request, pk):
    world = fake_data.world()
    posting = world.posting(pk)
    if posting is None:
        raise Http404("No such posting in the preview data")
    context = _context(
        request,
        world,
        "postings",
        posting=posting,
        reviews=world.reviews_for(posting),
        application=world.application_for(posting),
    )
    return render(request, "postings/detail.html", context)


def posting_add(request):
    world = fake_data.world()
    return render(request, "postings/add.html", _context(request, world, "postings"))
