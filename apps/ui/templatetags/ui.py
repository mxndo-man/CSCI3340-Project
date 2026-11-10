"""Template helpers for the Shortlist UI. Load them with {% load ui %}.

Every helper reads only the field names and choice values in docs/contracts.md, so it works
the same on the preview's fake objects and on the real models.
"""

import json
from datetime import date, time
from decimal import Decimal
from urllib.parse import urlencode

from django import template
from django.template.loader import render_to_string
from django.urls import NoReverseMatch, reverse
from django.utils import timezone
from django.utils.dateformat import format as date_format
from django.utils.timesince import timesince

register = template.Library()


# ---- Buttons, icons and form inputs -----------------------------------------------------

# One primary (clay) button per view; secondary and ghost for everything else.
BUTTON_BASE = (
    "inline-flex shrink-0 select-none items-center justify-center gap-2 whitespace-nowrap "
    "rounded-full font-semibold transition-colors disabled:cursor-not-allowed disabled:opacity-50"
)
BUTTON_KIND = {
    "primary": "bg-clay-600 text-white hover:bg-clay-700",
    "secondary": "border border-sand-300 bg-white text-bark-900 hover:bg-sand-100",
    "ghost": "text-bark-700 hover:bg-sand-100 hover:text-bark-900",
    "danger": "text-brick-700 hover:bg-brick-50",
}
BUTTON_SIZE = {"sm": "h-9 px-4 text-sm", "md": "h-11 px-5 text-[15px]"}


@register.simple_tag
def button_class(kind="secondary", size="md", extra=""):
    """Classes for a button, or a link that looks like one: {% button_class "primary" "sm" %}."""
    parts = (
        BUTTON_BASE,
        BUTTON_KIND.get(kind or "secondary", BUTTON_KIND["secondary"]),
        BUTTON_SIZE.get(size or "md", BUTTON_SIZE["md"]),
        extra,
    )
    return " ".join(part for part in parts if part)


@register.simple_tag
def icon(name, css="size-4", label=""):
    """An inline Lucide icon from templates/components/icons/. Decorative unless it gets a label."""
    return render_to_string(
        f"components/icons/{name}.html", {"class": css, "icon_label": label}
    )


# Text inputs, selects and textareas share one look. The border color is chosen once
# (normal or error) so two border colors never compete.
INPUT = (
    "w-full rounded-xl border bg-white px-3.5 text-[15px] text-bark-900 placeholder:text-bark-500 "
    "transition focus:border-clay-600 focus:outline-none focus:ring-3 focus:ring-clay-600/20"
)
WIDGET_SHAPE = {
    "select": "h-11 appearance-none pr-10",
    "textarea": "resize-y py-3",
}


@register.simple_tag
def ui_widget(field, has_hint=False, extra="", placeholder="", autocomplete=""):
    """Render one form field's input with the design classes, linked to its hint and errors.

    The ids match components/field.html: <id>_helptext and <id>_error.
    """
    if field.widget_type == "checkbox":
        css = "mt-0.5 size-4 shrink-0 accent-clay-600"
    else:
        border = "border-brick-700" if field.errors else "border-sand-400"
        css = f"{INPUT} {border} {WIDGET_SHAPE.get(field.widget_type, 'h-11')}"
    attrs = {"class": f"{css} {extra}".strip()}
    if placeholder:
        attrs["placeholder"] = placeholder
    if autocomplete:
        attrs["autocomplete"] = autocomplete
    described_by = []
    if has_hint:
        described_by.append(f"{field.auto_id}_helptext")
    if field.errors:
        described_by.append(f"{field.auto_id}_error")
    if described_by:
        attrs["aria-describedby"] = " ".join(described_by)
    return field.as_widget(attrs=attrs)


# ---- People -----------------------------------------------------------------------------

AVATAR_TONES = ("clay", "moss", "ochre", "sand")


@register.simple_tag
def display_name(person):
    """The name boards and comments show: display_name, or the username if it's blank."""
    return getattr(person, "display_name", "") or getattr(person, "username", "")


@register.simple_tag
def initials(person):
    """'Liam R.' -> 'LR'. A one-word name gives its first two letters."""
    name = display_name(person)
    words = name.replace(".", " ").split()
    if len(words) >= 2:
        return (words[0][0] + words[1][0]).upper()
    return name[:2].upper()


@register.simple_tag
def avatar_tone(person):
    """A stable avatar color per person, picked from their id."""
    key = getattr(person, "pk", None) or getattr(person, "id", None)
    if not key:
        return "sand"
    return AVATAR_TONES[(int(key) - 1) % len(AVATAR_TONES)]


@register.simple_tag
def first_name(person):
    """For greetings: first_name, else the first word of the display name or username."""
    return getattr(person, "first_name", "") or display_name(person).split(" ")[0]


# ---- Posting facts ----------------------------------------------------------------------

# Contract value -> (chip tone, chip label, the value written out on the posting page)
CITIZENSHIP = {
    "US_CITIZEN": ("alert", "US citizens only", "US citizens only"),
    "US_PERSON": ("warn", "US citizens or PR", "US citizens or permanent residents"),
    "WORK_AUTHORIZATION": (
        "warn",
        "Work authorization",
        "Must be authorized to work in the US",
    ),
    "NOT_SPECIFIED": ("good", "Any citizenship", "No requirement"),
}
CLEARANCE = {
    "NONE_MENTIONED": ("good", "No clearance", "Not required"),
    "ABLE_TO_OBTAIN": ("alert", "Clearance required", "Must be able to get one"),
    "ACTIVE_REQUIRED": ("alert", "Active clearance", "Must already have one"),
}
WORK_MODE = {
    "ONSITE": "On-site",
    "HYBRID": "Hybrid",
    "REMOTE": "Remote",
    "UNSPECIFIED": "Not stated",
}
DEGREE = {
    "HS": "High school",
    "ASSOCIATE": "Associate",
    "BACHELOR": "Bachelor's",
    "MASTER": "Master's",
    "PHD": "PhD",
}
PROVIDER = {"GREENHOUSE": "Greenhouse", "LEVER": "Lever", "ASHBY": "Ashby"}


def _amount(value):
    """Decimal("25.00") -> "25", 80000 -> "80,000", Decimal("25.5") -> "25.50"."""
    number = Decimal(value)
    if number == number.to_integral_value():
        return f"{int(number):,}"
    return f"{number:,.2f}"


def _pay_range(low, high):
    if low is None or low == high:
        return f"${_amount(high)}"
    return f"${_amount(low)}–{_amount(high)}"


def pay_text(pay_min, pay_max, pay_period):
    """The pay written out: "$32 an hour", "$25–29 an hour", "$80,000 a year", "Unpaid"."""
    high = pay_max if pay_max is not None else pay_min
    if high is None:
        return "Not stated"
    if not high:
        return "Unpaid"
    per = {"HOUR": " an hour", "YEAR": " a year"}.get(pay_period or "", "")
    return f"{_pay_range(pay_min, high)}{per}"


def degree_text(levels):
    """["BACHELOR", "MASTER"] -> "Bachelor's or Master's". An empty list means any degree."""
    names = [label for value, label in DEGREE.items() if value in (levels or [])]
    if not names:
        return "Any degree"
    if len(names) == 1:
        return names[0]
    return ", ".join(names[:-1]) + " or " + names[-1]


@register.simple_tag
def work_mode_label(value):
    return WORK_MODE.get(value or "", "")


@register.simple_tag
def provider_label(posting):
    """Which job board a posting came from, or "Added by a student"."""
    provider = getattr(getattr(posting, "source", None), "provider", None)
    return PROVIDER.get(provider or "", "Added by a student")


@register.simple_tag
def posting_chips(posting):
    """The deciding facts as chips: pay, clearance, citizenship and degree.

    Each is {"tone": ..., "label": ...}. Fields that haven't been read yet (null) are
    left out instead of guessed.
    """
    chips = []
    high = posting.pay_max if posting.pay_max is not None else posting.pay_min
    if high is not None:
        if high:
            per = {"HOUR": "/hr", "YEAR": "/yr"}.get(posting.pay_period or "", "")
            label = f"Paid · {_pay_range(posting.pay_min, high)}{per}"
            chips.append({"tone": "good", "label": label})
        else:
            chips.append({"tone": "alert", "label": "Unpaid"})
    for value, table in (
        (posting.clearance, CLEARANCE),
        (posting.citizenship, CITIZENSHIP),
    ):
        if value in table:
            tone, label, _ = table[value]
            chips.append({"tone": tone, "label": label})
    if getattr(posting, "extraction_status", "DONE") in ("DONE", "MANUAL"):
        chips.append({"tone": "neutral", "label": degree_text(posting.degree_levels)})
    return chips


@register.simple_tag
def boards_with(posting, boards):
    """The boards (from the page's my_boards) that already hold this posting.

    Reads each board's BoardPostings, so prefetch them: see docs/frontend-handoff.md.
    """
    return [
        b
        for b in boards or ()
        if any(item.posting_id == posting.id for item in board_postings(b))
    ]


# ---- The "Key facts" tiles on a posting page --------------------------------------------

FACTS = (
    ("deadline", "Deadline"),
    ("pay", "Pay"),
    ("citizenship", "Citizenship"),
    ("clearance", "Security clearance"),
    ("degree_levels", "Degree"),
    ("work_mode", "Work mode"),
    ("start_term", "Start term"),
    ("location", "Location"),
)
PAY_PERIOD = {"HOUR": "an hour", "YEAR": "a year", "UNKNOWN": "not stated"}


def _raw_value(posting, key):
    if key == "pay":
        return {
            "min": posting.pay_min,
            "max": posting.pay_max,
            "period": posting.pay_period,
        }
    return getattr(posting, key, None)


def _written(key, value, posting):
    """A field's value as the tile shows it."""
    if key == "deadline":
        if isinstance(value, str):  # a FieldReview's proposed_value is JSON
            value = date.fromisoformat(value)
        if value:
            return date_format(value, "F j, Y")
        return "Rolling" if posting.deadline_type == "ROLLING" else "Not stated"
    if key == "pay":
        value = value or {}
        return pay_text(value.get("min"), value.get("max"), value.get("period"))
    if key in ("citizenship", "clearance"):
        table = CITIZENSHIP if key == "citizenship" else CLEARANCE
        return table[value][2] if value in table else "Not read yet"
    if key == "degree_levels":
        return degree_text(value)
    if key == "work_mode":
        return WORK_MODE.get(value or "", "Not read yet")
    return value or "Not stated"


def _fix_form(key, value):
    """What the tile's "Fix it" form needs: which input, its choices, its start value."""
    if key == "deadline":
        initial = value.isoformat() if isinstance(value, date) else (value or "")
        return {"input": "date", "initial": initial, "choices": ()}
    if key == "pay":
        return {"input": "pay", "initial": value or {}, "choices": PAY_PERIOD.items()}
    if key in ("citizenship", "clearance"):
        table = CITIZENSHIP if key == "citizenship" else CLEARANCE
        choices = [(code, labels[2]) for code, labels in table.items()]
        return {"input": "select", "initial": value or "", "choices": choices}
    if key == "work_mode":
        return {"input": "select", "initial": value or "", "choices": WORK_MODE.items()}
    if key == "degree_levels":
        return {
            "input": "checkboxes",
            "initial": value or [],
            "choices": DEGREE.items(),
        }
    return {"input": "text", "initial": value or "", "choices": ()}


@register.simple_tag
def fact_source(posting, field_name, review=None):
    """Where a fact came from: "From Greenhouse", "Read by AI · 94% sure", "Checked by a
    student". Reads Posting.field_sources and the confidence in Posting.field_details.
    A pending FieldReview reports its own confidence."""
    if review is not None:
        return f"Read by AI · {round(review.confidence * 100)}% sure"
    source = (posting.field_sources or {}).get(field_name)
    detail = (posting.field_details or {}).get(field_name) or {}
    if source == "user":
        return "Checked by a student"
    if source == "api":
        return f"From {provider_label(posting)}"
    if source in ("model", "rules"):
        reader = "AI" if source == "model" else "our rules"
        confidence = detail.get("confidence")
        if confidence is None:
            return f"Read by {reader}"
        return f"Read by {reader} · {round(confidence * 100)}% sure"
    return "Not read yet"


@register.simple_tag
def facts_for(posting, reviews=()):
    """The eight "Key facts" tiles for a posting page, in order.

    reviews: the posting's pending FieldReviews. A field with one shows the AI's
    proposed value, its confidence and its evidence, and gets Looks right / Fix it.
    Other fields read the posting, with the evidence from Posting.field_details.
    Each tile is a dict: key, label, value, source, quote, needs_check, review, plus
    input, choices and initial for the fix form.
    """
    pending = {r.field_name: r for r in reviews or () if r.status == "PENDING"}
    details = posting.field_details or {}
    facts = []
    for key, label in FACTS:
        review = pending.get(key)
        value = review.proposed_value if review else _raw_value(posting, key)
        evidence = (
            review.evidence if review else (details.get(key) or {}).get("evidence")
        )
        facts.append(
            {
                "key": key,
                "label": label,
                "value": _written(key, value, posting),
                "source": fact_source(posting, key, review),
                "quote": evidence or "",
                "needs_check": review is not None,
                "review": review,
                **_fix_form(key, value),
            }
        )
    return facts


# ---- Discover's filters -----------------------------------------------------------------

# key, label, and options: (value sent, menu label, chip label, phrase in a search's name).
# Lists are sent comma-separated; see apps/ui_preview/filters.py.
DISCOVER_MENUS = (
    (
        "citizenship",
        "Citizenship",
        (
            (
                "NOT_SPECIFIED,WORK_AUTHORIZATION",
                "No citizenship requirement",
                "No requirement",
                "no citizenship requirement",
            ),
            (
                "NOT_SPECIFIED,WORK_AUTHORIZATION,US_PERSON",
                "Open to permanent residents",
                "PR OK",
                "open to permanent residents",
            ),
        ),
    ),
    (
        "degree_levels",
        "Degree",
        (
            ("BACHELOR", "I'm working toward a bachelor's", "Bachelor's", "bachelor's"),
            ("MASTER", "I'm working toward a master's", "Master's", "master's"),
        ),
    ),
    (
        "work_mode",
        "Work mode",
        (
            ("REMOTE", "Remote", "Remote", "remote"),
            ("HYBRID", "Hybrid", "Hybrid", "hybrid"),
            ("ONSITE", "On-site", "On-site", "on-site"),
        ),
    ),
)


def _chosen(filters, key):
    value = filters.get(key) or ""
    return ",".join(value) if isinstance(value, (list, tuple)) else value


def _all_menus(start_terms):
    terms = tuple((term, term, term, term.lower()) for term in start_terms or ())
    return DISCOVER_MENUS + (("start_term", "Start term", terms),)


@register.simple_tag
def discover_menus(filters, start_terms=()):
    """Discover's filter menus, each with its options and the one that's chosen.

    start_terms: the start terms that exist in the data, for the last menu.
    """
    menus = []
    for key, label, options in _all_menus(start_terms):
        chosen = _chosen(filters, key)
        items = [
            {"value": value, "label": text, "short": short, "selected": value == chosen}
            for value, text, short, _ in options
        ]
        selected = next((item for item in items if item["selected"]), None)
        menus.append(
            {"key": key, "label": label, "options": items, "selected": selected}
        )
    return menus


@register.simple_tag
def active_filter_count(filters):
    """How many filters are on (the search box doesn't count)."""
    keys = (
        "paid",
        "deadline_within_days",
        "start_term",
        *(m[0] for m in DISCOVER_MENUS),
    )
    return sum(1 for key in keys if filters.get(key)) + bool(filters.get("clearance"))


@register.simple_tag
def describe_filters(filters, start_terms=()):
    """A readable name for a search: "Paid, no clearance, closes within 30 days"."""
    parts = []
    if filters.get("q"):
        parts.append(f"“{filters['q']}”")
    if filters.get("paid"):
        parts.append("paid")
    if filters.get("clearance") == ["NONE_MENTIONED"]:
        parts.append("no clearance")
    if filters.get("deadline_within_days"):
        parts.append(f"closes within {filters['deadline_within_days']} days")
    for key, _, options in DISCOVER_MENUS:
        chosen = _chosen(filters, key)
        parts.extend(phrase for value, _, _, phrase in options if value == chosen)
    if filters.get("start_term"):
        parts.append(filters["start_term"].lower())
    text = ", ".join(parts)
    return text[:1].upper() + text[1:] if text else "All internships"


@register.filter
def filters_json(filters):
    """The filters that are set, as JSON: the value a SavedSearch stores."""
    return json.dumps({key: value for key, value in filters.items() if value})


# ---- Dates ------------------------------------------------------------------------------


@register.simple_tag
def countdown(posting_or_date):
    """How long until a deadline: {"text": "3 days left", "tone": "urgent", "days": 3, ...}.

    Takes a posting (reads deadline, deadline_type and status) or a plain date.
    Tones: urgent (5 days or fewer), soon (10 or fewer), calm, closed.
    """
    deadline = getattr(posting_or_date, "deadline", posting_or_date)
    deadline_type = getattr(posting_or_date, "deadline_type", None)
    closed = getattr(posting_or_date, "status", "OPEN") == "CLOSED"
    if deadline is None:
        text = (
            "Rolling deadline" if deadline_type == "ROLLING" else "No deadline listed"
        )
        return {"text": text, "headline": text, "tone": "calm", "days": None}
    days = (deadline - timezone.localdate()).days
    if closed or days < 0:
        return {
            "text": "Closed",
            "headline": "This posting has closed",
            "tone": "closed",
            "days": days,
        }
    if days == 0:
        return {
            "text": "Closes today",
            "headline": "Closes today",
            "tone": "urgent",
            "days": 0,
        }
    text = "1 day left" if days == 1 else f"{days} days left"
    headline = "Closes tomorrow" if days == 1 else f"Closes in {days} days"
    tone = "urgent" if days <= 5 else "soon" if days <= 10 else "calm"
    return {"text": text, "headline": headline, "tone": tone, "days": days}


# ---- Links to pages ---------------------------------------------------------------------

# Contract URL names (docs/contracts.md section 7) and the preview page for each one.
# notifications:preferences isn't in section 7 yet; it's proposed in the handoff doc.
# Delete this map when the preview app goes away.
PREVIEW_PAGES = {
    "home": "ui_preview:home",
    "postings:discover": "ui_preview:discover",
    "postings:add": "ui_preview:posting_add",
    "boards:list": "ui_preview:boards",
    "tracker:applications": "ui_preview:applications",
    "tracker:tasks": "ui_preview:tasks",
    "notifications:list": "ui_preview:notifications",
    "notifications:saved_searches": "ui_preview:saved_searches",
    "notifications:preferences": "ui_preview:preferences",
}


def _reverse_first(names, args):
    for name in names:
        if not name:
            continue
        try:
            return reverse(name, args=args)
        except NoReverseMatch:
            continue
    return ""


@register.simple_tag(takes_context=True)
def page_url(context, name, *args):
    """Link to a page by its contract URL name, or "" if nothing serves it yet.

    On a real page it's the real URL only, so a page nobody has built yet shows as plain
    text (and a real user never lands in the preview as the fake user). On a preview page
    it's the preview's stand-in, so a demo stays inside the preview.
    """
    if context.get("ui_preview"):
        return _reverse_first([PREVIEW_PAGES.get(name), name], args)
    return _reverse_first([name], args)


# Forms that already have a real URL to post to. An action that isn't here gets its URL
# from the view's form_urls (see docs/frontend-handoff.md); add it here once it exists.
FORM_URL_NAMES = {
    "create_board": "boards:create",
    "join_board": "boards:join",
    "leave_board": "boards:leave",
    "remove_member": "boards:remove",
}


@register.simple_tag(takes_context=True)
def form_url(context, action, *args):
    """Where a form posts: {% form_url "leave_board" board.pk as url %}.

    The view's form_urls wins, so the preview can send every form to its no-op handler.
    Otherwise it's the real URL in FORM_URL_NAMES, or "" if that doesn't exist yet.
    """
    given = (context.get("form_urls") or {}).get(action)
    if given:
        return given
    return _reverse_first([FORM_URL_NAMES.get(action)], args)


MAIN_NAV = (
    ("Discover", "postings:discover", "postings"),
    ("Boards", "boards:list", "boards"),
    ("Tracker", "tracker:applications", "tracker"),
)


@register.simple_tag(takes_context=True)
def main_nav(context):
    """The top bar's links. Logged out shows Discover only.

    The active link comes from the URL's app (request.resolver_match.app_name), or from a
    `nav_active` context variable on pages outside those apps, like the previews.
    """
    request = context.get("request")
    match = getattr(request, "resolver_match", None)
    section = context.get("nav_active") or getattr(match, "app_name", "")
    user = context.get("user")
    items = MAIN_NAV if user is not None and user.is_authenticated else MAIN_NAV[:1]
    return [
        {"label": label, "url": page_url(context, name), "active": section == app}
        for label, name, app in items
    ]


# ---- Boards -----------------------------------------------------------------------------


# These read the contracts' relations (Membership and BoardPosting have no related_name, so
# Django names them membership_set and boardposting_set). The view only has to prefetch
# them; it doesn't have to add anything to the board.


def _related(obj, name):
    """obj.<name>.all() as a list, or [] if that relation doesn't exist yet."""
    manager = getattr(obj, name, None)
    return list(manager.all()) if manager is not None else []


@register.simple_tag
def memberships(board):
    """The board's Memberships, owners first, then in the order people joined."""
    rows = _related(board, "membership_set")
    return sorted(rows, key=lambda m: (m.role != "OWNER", m.joined_at))


@register.simple_tag
def board_members(board):
    """The board's members (users), owners first."""
    return [m.user for m in memberships(board)]


@register.simple_tag
def member_count(board):
    return len(_related(board, "membership_set"))


@register.simple_tag
def board_role(board, user):
    """The user's role on the board: "OWNER", "MEMBER", or "" if they aren't on it."""
    user_id = getattr(user, "pk", None) or getattr(user, "id", None)
    return next(
        (m.role for m in _related(board, "membership_set") if m.user_id == user_id), ""
    )


@register.simple_tag
def board_postings(board):
    """The board's BoardPostings, newest first."""
    rows = _related(board, "boardposting_set")
    return sorted(rows, key=lambda bp: bp.saved_at, reverse=True)


@register.simple_tag
def member_overflow(board, shown=4):
    """How many members the avatar stack leaves out: the "+10" circle."""
    return max(member_count(board) - shown, 0)


# ---- Tracker ----------------------------------------------------------------------------

# Application.status, in pipeline order. The first five are the board's columns; the last
# two are the "Closed" list under it.
APPLICATION_STATUSES = (
    ("SAVED", "Saved"),
    ("APPLYING", "Applying"),
    ("APPLIED", "Applied"),
    ("INTERVIEW", "Interview"),
    ("OFFER", "Offer"),
    ("REJECTED", "Rejected"),
    ("WITHDRAWN", "Withdrawn"),
)
CLOSED_STATUSES = ("REJECTED", "WITHDRAWN")


@register.simple_tag
def application_statuses():
    """Every status as (value, label), for the "Move to" menu."""
    return APPLICATION_STATUSES


@register.simple_tag
def tracker_columns(applications):
    """The board's five columns, each {"status", "label", "applications"}."""
    return [
        {
            "status": status,
            "label": label,
            "applications": [a for a in applications or () if a.status == status],
        }
        for status, label in APPLICATION_STATUSES
        if status not in CLOSED_STATUSES
    ]


@register.simple_tag
def closed_applications(applications):
    """Rejected and withdrawn applications, most recently changed first."""
    closed = [a for a in applications or () if a.status in CLOSED_STATUSES]
    return sorted(closed, key=lambda a: a.updated_at, reverse=True)


@register.simple_tag
def active_count(applications):
    """Applications still in progress: everything but rejected and withdrawn."""
    return sum(1 for a in applications or () if a.status not in CLOSED_STATUSES)


def _local(moment):
    return timezone.localtime(moment) if timezone.is_aware(moment) else moment


@register.simple_tag
def next_task(application):
    """The application's soonest open Task (through task_set), or None."""
    open_tasks = [t for t in _related(application, "task_set") if not t.done]
    return min(open_tasks, key=lambda t: t.due_at, default=None)


@register.simple_tag
def application_line(application):
    """The one line under an application card's company: what's next for it."""
    status = application.status
    if status == "INTERVIEW" and application.next_step_at:
        when = date_format(_local(application.next_step_at), "D, M j · g:i A")
        return f"Interview {when}"
    if status == "OFFER":
        return "Offer received. Congrats!"
    if status in CLOSED_STATUSES:
        verb = "Not selected" if status == "REJECTED" else "You withdrew"
        return f"{verb} · {date_format(_local(application.updated_at), 'M j')}"
    if status == "APPLIED" and application.applied_on:
        return f"Applied {date_format(application.applied_on, 'M j')}"
    task = next_task(application)
    if task is not None:
        return f"{task.title} · due {date_format(_local(task.due_at), 'D, M j')}"
    posting = application.posting
    if posting.deadline:
        return f"Closes {date_format(posting.deadline, 'M j')} · {countdown(posting)['text']}"
    return "No deadline listed"


@register.simple_tag
def task_due(task):
    """{"text": "Due Thu, Nov 5", "urgent": True}. Urgent: open and due within 2 days."""
    due = _local(task.due_at)
    days = (due.date() - timezone.localdate()).days
    return {
        "text": f"Due {date_format(due, 'D, M j')}",
        "urgent": not task.done and days <= 2,
    }


@register.simple_tag
def split_tasks(tasks):
    """{"open": [...] soonest first, "done": [...]}."""
    tasks = list(tasks or ())
    return {
        "open": sorted((t for t in tasks if not t.done), key=lambda t: t.due_at),
        "done": [t for t in tasks if t.done],
    }


@register.simple_tag
def due_this_week(tasks):
    """Open tasks due from today through the next 7 days, soonest first."""
    today = timezone.localdate()
    soon = [
        t
        for t in tasks or ()
        if not t.done and 0 <= (_local(t.due_at).date() - today).days <= 7
    ]
    return sorted(soon, key=lambda t: t.due_at)


# ---- Notifications and saved searches ---------------------------------------------------

NOTIFICATION_ICON = {
    "TASK_DUE": "list-checks",
    "DEADLINE_SOON": "clock",
    "NEW_MATCH": "compass",
    "POSTING_CLOSED": "lock",
}


@register.simple_tag
def notification_icon(kind):
    """The icon name for a Notification.kind."""
    return NOTIFICATION_ICON.get(kind, "bell")


# Discover's list filters travel comma-separated: ?work_mode=REMOTE,HYBRID. These must match
# how Discover reads them (apps/ui_preview/filters.py now, apps/postings/filters.py later).
LIST_FILTERS = ("citizenship", "clearance", "degree_levels", "work_mode")


@register.filter
def discover_query(filters):
    """A SavedSearch.filters dict as Discover's query string: {{ search.filters|discover_query }}."""
    pairs = [("applied", "1")]
    for key, value in (filters or {}).items():
        if not value:
            continue
        if key == "paid":
            pairs.append((key, "1"))
        elif key in LIST_FILTERS:
            pairs.append((key, ",".join(value)))
        else:
            pairs.append((key, str(value)))
    return urlencode(pairs)


@register.simple_tag
def saved_search_line(search):
    """The line under a saved search's name: whether alerts are on, and when they last ran."""
    if not search.alerts_enabled:
        return "Alerts are off"
    if search.last_alerted_at:
        return f"Alerts are on · last checked {timesince(search.last_alerted_at)} ago"
    return "Alerts are on · new matches show up in your daily digest"


@register.simple_tag
def digest_hours():
    """(hour, label) for every NotificationPreference.digest_hour: (8, "8:00 AM")."""
    return [(hour, date_format(time(hour), "g:i A")) for hour in range(24)]


@register.simple_tag
def unread_count(notifications):
    return sum(1 for n in notifications or () if not n.read)
