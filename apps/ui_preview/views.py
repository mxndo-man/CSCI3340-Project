"""The preview pages: real templates rendered with fake objects from fake_data.py.

The notifications page is an exception: it displays the signed-in user's real
notifications and uses the real mark-as-read actions.

The pages show the sample data on whoever is logged in. Pages that need an account in the
real app (the prototype's home, add, boards, tracker and settings) send logged-out
visitors to log in, the same way the real views will.
"""

from datetime import timedelta

from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from apps.notifications.models import Notifications
from apps.ui.templatetags import ui

from . import fake_data
from .filters import SORTS, filter_postings, parse_filters

# ---- Preview pages ----------------------------------------------------------------------

# Every form the templates post. The preview sends them all to `action`; on real pages
# {% form_url %} finds the real URL instead. docs/frontend-handoff.md lists each form.
FORM_ACTIONS = (
    "save_to_board",
    "remove_from_board",
    "track",
    "review_field",
    "add_posting",
    "save_search",
    "create_board",
    "join_board",
    "leave_board",
    "remove_member",
    "comment",
    "move_application",
    "add_task",
    "toggle_task",
    "toggle_alerts",
    "delete_saved_search",
    "update_preferences",
    "mark_all_read",
    "open_notification",
)


def _world(request):
    """The sample data, with the logged-in user (if any) as "you"."""
    return fake_data.world(request.user if request.user.is_authenticated else None)


def _context(request, world, nav_active="", **extra):
    """What every preview page gets. Logged out, or with ?as=visitor on a public page, it's
    the logged-out version."""
    visitor = not request.user.is_authenticated or request.GET.get("as") == "visitor"
    action_url = reverse("ui_preview:action")
    context = {
        "ui_preview": True,
        "nav_active": nav_active,
        "user": AnonymousUser() if visitor else world.me,
        "form_urls": dict.fromkeys(FORM_ACTIONS, action_url),
        "my_boards": [] if visitor else world.my_boards(),
        # The bell. A real context processor in apps/notifications adds this to every page.
        "notification_menu": None if visitor else world.notification_menu(),
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


# The pages listed on /preview/: label, URL name, URL args, template.
INDEX_PAGES = [
    ("Home", "ui_preview:home", [], "pages/home.html"),
    ("Home for a brand-new user", "ui_preview:home_new", [], "pages/home.html"),
    ("Discover", "ui_preview:discover", [], "postings/discover.html"),
    (
        "A posting with a fact to check",
        "ui_preview:posting_detail",
        [1],
        "postings/detail.html",
    ),
    (
        "A posting with two facts to check",
        "ui_preview:posting_detail",
        [8],
        "postings/detail.html",
    ),
    ("A closed posting", "ui_preview:posting_detail", [12], "postings/detail.html"),
    ("Add a posting", "ui_preview:posting_add", [], "postings/add.html"),
    ("Boards", "ui_preview:boards", [], "boards/list.html"),
    (
        "A board you own, with comments",
        "ui_preview:board_detail",
        [1],
        "boards/detail.html",
    ),
    (
        "A board you're a member of",
        "ui_preview:board_detail",
        [3],
        "boards/detail.html",
    ),
    ("New board (its own page)", "ui_preview:board_create", [], "boards/create.html"),
    ("Join a board (its own page)", "ui_preview:board_join", [], "boards/join.html"),
    (
        "Tracker: applications by status",
        "ui_preview:applications",
        [],
        "tracker/applications.html",
    ),
    ("Tracker: tasks", "ui_preview:tasks", [], "tracker/tasks.html"),
    ("Notifications", "ui_preview:notifications", [], "notifications/list.html"),
    (
        "Saved searches",
        "ui_preview:saved_searches",
        [],
        "notifications/saved_searches.html",
    ),
    (
        "Notification settings",
        "ui_preview:preferences",
        [],
        "notifications/preferences.html",
    ),
]


def index(request):
    """A list of every preview page."""
    world = _world(request)
    pages = [
        (label, reverse(name, args=args), template)
        for label, name, args, template in INDEX_PAGES
    ]
    return render(
        request, "ui_preview/index.html", _context(request, world, pages=pages)
    )


def discover(request):
    world = _world(request)
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
    world = _world(request)
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


@login_required
def posting_add(request):
    world = _world(request)
    return render(request, "postings/add.html", _context(request, world, "postings"))


@login_required
def boards(request):
    world = _world(request)
    context = _context(request, world, "boards", boards=world.my_boards())
    return render(request, "boards/list.html", context)


@login_required
def board_detail(request, pk):
    world = _world(request)
    board = world.board(pk)
    if board is None:
        raise Http404("No such board in the preview data")
    board_postings = ui.board_postings(board)
    chosen = request.GET.get("item", "")
    selected = next((bp for bp in board_postings if str(bp.id) == chosen), None)
    if selected is None and board_postings:
        selected = board_postings[0]
    context = _context(
        request,
        world,
        "boards",
        board=board,
        board_postings=board_postings,
        selected=selected,
        comments=world.comments_on(selected) if selected else [],
    )
    return render(request, "boards/detail.html", context)


# The same fields as apps/boards/forms.py, so the pages show the real labels and errors.
class BoardForm(forms.Form):
    name = forms.CharField(max_length=100)
    description = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 2}), required=False
    )


class JoinBoardForm(forms.Form):
    join_code = forms.CharField(max_length=12, label="Join code")


def _preview_form_page(request, form_class, template):
    """GET shows the form; POST shows its errors, or says nothing was saved."""
    world = _world(request)
    form = form_class(request.POST or None)
    if request.method == "POST" and form.is_valid():
        messages.info(request, "Preview only, nothing was saved")
        return redirect("ui_preview:boards")
    return render(request, template, _context(request, world, "boards", form=form))


@login_required
def board_create(request):
    return _preview_form_page(request, BoardForm, "boards/create.html")


@login_required
def board_join(request):
    return _preview_form_page(request, JoinBoardForm, "boards/join.html")


@login_required
def applications(request):
    world = _world(request)
    context = _context(
        request,
        world,
        "tracker",
        applications=world.applications,
        tasks=world.tasks,
    )
    return render(request, "tracker/applications.html", context)


@login_required
def tasks(request):
    world = _world(request)
    context = _context(request, world, "tracker", tasks=world.tasks)
    return render(request, "tracker/tasks.html", context)


@login_required
def notifications(request):
    world = _world(request)
    notifications = Notifications.objects.filter(recipient_id=request.user.pk)
    context = _context(request, world, notifications=notifications)
    context["notification_menu"] = {
        "notifications": notifications[:5],
        "unread_count": notifications.filter(is_read=False).count(),
    }
    context["form_urls"].update(
        {
            "mark_all_read": reverse("notifications:mark_all_read"),
            "open_notification": reverse("notifications:open_notification"),
        }
    )
    context["ui_preview_live_notifications"] = True
    return render(request, "notifications/list.html", context)


@login_required
def saved_searches(request):
    world = _world(request)
    context = _context(request, world, saved_searches=world.saved_searches)
    return render(request, "notifications/saved_searches.html", context)


@login_required
def preferences(request):
    world = _world(request)
    context = _context(request, world, preferences=world.preferences)
    return render(request, "notifications/preferences.html", context)


@login_required
def home(request, newcomer=False):
    """The home dashboard. /preview/home/new/ shows it for a brand-new user with nothing yet."""
    world = _world(request)
    search = (
        None
        if newcomer
        else next((s for s in world.saved_searches if s.alerts_enabled), None)
    )
    context = _context(
        request,
        world,
        closing=[] if newcomer else world.closing(),
        saved_search=search,
        new_matches=world.new_matches(search) if search else [],
        applications=[] if newcomer else world.applications,
        tasks=[] if newcomer else world.tasks,
        activity=[] if newcomer else world.activity(),
    )
    if newcomer:
        context["my_boards"] = []
        context["notification_menu"] = {"notifications": [], "unread_count": 0}
    return render(request, "pages/home.html", context)
