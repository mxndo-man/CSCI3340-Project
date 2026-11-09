"""The style guide (every UI component on one page) and the preview pages.

Preview pages render the real templates with fake objects from fake_data.py, so the UI works
before the models exist. Nothing here touches the database.
"""

from datetime import timedelta
from pathlib import Path
from types import SimpleNamespace

from django import forms
from django.conf import settings
from django.shortcuts import render
from django.utils import timezone


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
