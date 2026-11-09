"""Template helpers for the Shortlist UI. Load them with {% load ui %}.

Every helper reads only the field names and choice values in docs/contracts.md, so it works
the same on the preview's fake objects and on the real models.
"""

from django import template
from django.template.loader import render_to_string
from django.urls import NoReverseMatch, reverse
from django.utils import timezone

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
def ui_widget(field, has_hint=False, extra=""):
    """Render one form field's input with the design classes, linked to its hint and errors.

    The ids match components/field.html: <id>_helptext and <id>_error.
    """
    if field.widget_type == "checkbox":
        css = "mt-0.5 size-4 shrink-0 accent-clay-600"
    else:
        border = "border-brick-700" if field.errors else "border-sand-400"
        css = f"{INPUT} {border} {WIDGET_SHAPE.get(field.widget_type, 'h-11')}"
    attrs = {"class": f"{css} {extra}".strip()}
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
