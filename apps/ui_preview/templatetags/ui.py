"""Template helpers for the Shortlist UI. Load them with {% load ui %}.

Every helper reads only the field names and choice values in docs/contracts.md, so it works
the same on the preview's fake objects and on the real models.
"""

import json
from datetime import date
from decimal import Decimal

from django import template
from django.template.loader import render_to_string
from django.urls import NoReverseMatch, reverse
from django.utils import timezone
from django.utils.dateformat import format as date_format

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

    Each board needs a `posting_ids` set; see docs/frontend-handoff.md.
    """
    return [b for b in boards or () if posting.id in getattr(b, "posting_ids", ())]


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

# Contract URL names (docs/contracts.md section 7) and the preview page that stands in for
# each one until its owner builds it. Delete this map when the preview app goes away.
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

    Real pages win. Until a page exists, its preview stands in (when UI_PREVIEW is on).
    Preview pages link to other preview pages, so a demo stays inside the preview.
    """
    stand_in = PREVIEW_PAGES.get(name)
    names = [stand_in, name] if context.get("ui_preview") else [name, stand_in]
    return _reverse_first(names, args)


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
