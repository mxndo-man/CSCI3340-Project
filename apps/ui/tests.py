"""Tests for the shared UI: the project pages, base.html, the ui helpers, and the contract
between the templates and the real models.

config/urls.py reads UI_PREVIEW and DEBUG once, when it's imported, so these tests load
fresh copies of it under each setting (see urlconf()).
"""

import importlib.util
import sys
from datetime import date, datetime, timedelta
from decimal import Decimal
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.utils import timezone

from apps.ui.templatetags import ui


def urlconf(name, **flags):
    """Load config/urls.py as module `name` with these settings, and return the name."""
    if name not in sys.modules:
        with override_settings(**flags):
            path = Path(settings.BASE_DIR) / "config" / "urls.py"
            spec = importlib.util.spec_from_file_location(name, path)
            assert spec and spec.loader
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            sys.modules[name] = module
    return name


DEV = urlconf("tests_urls_dev", UI_PREVIEW=True, DEBUG=True)
LIVE = urlconf("tests_urls_live", UI_PREVIEW=False, DEBUG=False)


def status_of(response):
    """The response's status code. (Without Django's type stubs, pyright thinks the test
    client returns a request, so reading .status_code inline fails the type check.)"""
    return response.status_code


def body_of(response):
    """The response's HTML as text, for the same reason as status_of."""
    return response.content.decode()


def make_user(**fields):
    defaults = {
        "username": "ana",
        "email": "ana@example.test",
        "display_name": "Ana Z.",
    }
    return get_user_model().objects.create_user(
        password="pw-12345678", **{**defaults, **fields}
    )


@override_settings(ROOT_URLCONF=LIVE)
class ProjectPagesTests(TestCase):
    def test_landing_shows_for_visitors(self):
        response = self.client.get("/")
        self.assertEqual(status_of(response), 200)
        self.assertTemplateUsed(response, "pages/landing.html")
        self.assertContains(response, "Sign up")

    def test_landing_sends_logged_in_users_home(self):
        self.client.force_login(make_user())
        self.assertRedirects(self.client.get("/"), "/home/")

    def test_home_needs_log_in(self):
        response = self.client.get("/home/")
        self.assertRedirects(response, "/accounts/login/?next=/home/")

    def test_home_shows_when_logged_in(self):
        self.client.force_login(make_user())
        response = self.client.get("/home/")
        self.assertEqual(status_of(response), 200)
        self.assertContains(response, "Welcome, Ana")

    def test_base_logged_out(self):
        response = self.client.get("/accounts/login/")
        self.assertContains(response, 'href="#main"')  # the skip link
        self.assertContains(response, "Sign up")
        self.assertNotContains(response, "Account menu")

    def test_base_logged_in(self):
        self.client.force_login(make_user())
        response = self.client.get("/accounts/profile/")
        self.assertContains(response, "Account menu")
        self.assertContains(response, "Ana Z.")
        # Log out is a POST form, never a link.
        self.assertContains(response, 'action="/accounts/logout/"')

    def test_with_the_preview_off_real_pages_never_link_into_it(self):
        self.client.force_login(make_user())
        response = self.client.get("/accounts/profile/")
        self.assertNotContains(response, "/preview/")
        self.assertNotContains(response, "Preview:")

    @override_settings(ROOT_URLCONF=DEV)
    def test_with_the_preview_on_every_nav_link_works(self):
        # Discover, Boards and Tracker have no real views yet. With UI_PREVIEW on they must
        # still be links (to their previews), not plain text.
        self.client.force_login(make_user())
        response = self.client.get("/accounts/profile/")
        page = body_of(response)
        for label in ("Discover", "Boards", "Tracker"):
            with self.subTest(label=label):
                self.assertRegex(page, rf'<a href="/[^"]+"[^>]*>\s*{label}\s')
        # The real page itself isn't a preview, so no preview banner.
        self.assertNotContains(response, "Preview:")

    def test_styleguide_is_off_without_debug(self):
        self.assertEqual(status_of(self.client.get("/styleguide/")), 404)

    @override_settings(ROOT_URLCONF=DEV)
    def test_styleguide_is_on_with_debug(self):
        response = self.client.get("/styleguide/")
        self.assertEqual(status_of(response), 200)
        self.assertTemplateUsed(response, "ui/styleguide.html")


class LinkHelperTests(TestCase):
    @override_settings(ROOT_URLCONF=DEV)
    def test_page_url_on_a_preview_page_uses_the_stand_in(self):
        self.assertEqual(
            ui.page_url({"ui_preview": True}, "boards:list"), "/preview/boards/"
        )

    @override_settings(ROOT_URLCONF=DEV)
    def test_page_url_on_a_real_page_falls_back_to_the_preview(self):
        with mock.patch.dict(ui.PREVIEW_PAGES, {"not_built:page": "ui_preview:boards"}):
            self.assertEqual(ui.page_url({}, "not_built:page"), "/preview/boards/")

    @override_settings(ROOT_URLCONF=DEV)
    def test_page_url_prefers_the_real_page_to_its_preview(self):
        with mock.patch.dict(
            ui.PREVIEW_PAGES, {"accounts:profile": "ui_preview:boards"}
        ):
            self.assertEqual(ui.page_url({}, "accounts:profile"), "/accounts/profile/")

    @override_settings(ROOT_URLCONF=LIVE)
    def test_page_url_with_the_preview_off_is_empty_for_unbuilt_pages(self):
        with mock.patch.dict(ui.PREVIEW_PAGES, {"not_built:page": "ui_preview:boards"}):
            self.assertEqual(ui.page_url({}, "not_built:page"), "")

    def test_page_url_finds_real_pages(self):
        self.assertEqual(ui.page_url({}, "accounts:profile"), "/accounts/profile/")
        self.assertEqual(ui.page_url({}, "no_such:page"), "")

    def test_form_url_prefers_the_views_form_urls(self):
        context = {"form_urls": {"create_board": "/somewhere/"}}
        self.assertEqual(ui.form_url(context, "create_board"), "/somewhere/")

    def test_form_url_falls_back_to_the_real_url(self):
        with mock.patch.dict(ui.FORM_URL_NAMES, {"edit_profile": "accounts:profile"}):
            self.assertEqual(ui.form_url({}, "edit_profile"), "/accounts/profile/")
        self.assertEqual(ui.form_url({}, "not_built_yet"), "")


class PostingHelperTests(TestCase):
    def test_pay_text(self):
        self.assertEqual(
            ui.pay_text(Decimal(25), Decimal(32), "HOUR"), "$25–32 an hour"
        )
        self.assertEqual(ui.pay_text(None, 80000, "YEAR"), "$80,000 a year")
        self.assertEqual(ui.pay_text(0, 0, "HOUR"), "Unpaid")
        self.assertEqual(ui.pay_text(None, None, None), "Not stated")

    def test_degree_text(self):
        self.assertEqual(
            ui.degree_text(["MASTER", "BACHELOR"]), "Bachelor's or Master's"
        )
        self.assertEqual(ui.degree_text([]), "Any degree")

    def test_countdown_tones(self):
        today = timezone.localdate()
        cases = [(0, "urgent", "Closes today"), (5, "urgent", "5 days left"),
                 (6, "soon", "6 days left"), (11, "calm", "11 days left"), (-1, "closed", "Closed")]  # fmt: skip
        for days, tone, text in cases:
            with self.subTest(days=days):
                result = ui.countdown(today + timedelta(days=days))
                self.assertEqual((result["tone"], result["text"]), (tone, text))
        rolling = SimpleNamespace(deadline=None, deadline_type="ROLLING", status="OPEN")
        self.assertEqual(ui.countdown(rolling)["text"], "Rolling deadline")

    def test_chips_leave_out_fields_not_read_yet(self):
        posting = SimpleNamespace(
            pay_min=None, pay_max=None, pay_period=None, clearance=None, citizenship=None,
            degree_levels=[], extraction_status="PENDING",
        )  # fmt: skip
        self.assertEqual(ui.posting_chips(posting), [])


def related(*rows):
    """A stand-in for a reverse relation: obj.<name>.all()."""
    return SimpleNamespace(all=lambda: list(rows))


class BoardHelperTests(TestCase):
    def setUp(self):
        now = timezone.now()
        self.owner = SimpleNamespace(id=1, pk=1, display_name="Ana Z.")
        self.member = SimpleNamespace(id=2, pk=2, display_name="Ben Y.")
        rows = [
            SimpleNamespace(user=self.member, user_id=2, role="MEMBER", joined_at=now),
            SimpleNamespace(user=self.owner, user_id=1, role="OWNER", joined_at=now),
        ]
        self.board = SimpleNamespace(membership_set=related(*rows))

    def test_members_owner_first(self):
        self.assertEqual(ui.board_members(self.board), [self.owner, self.member])
        self.assertEqual(ui.member_count(self.board), 2)

    def test_roles(self):
        self.assertEqual(ui.board_role(self.board, self.owner), "OWNER")
        self.assertEqual(ui.board_role(self.board, self.member), "MEMBER")
        self.assertEqual(ui.board_role(self.board, SimpleNamespace(id=3, pk=3)), "")

    def test_a_board_without_boardpostings_yet(self):
        # The boards app ships before BoardPosting exists; the helpers must cope.
        self.assertEqual(ui.board_postings(self.board), [])
        self.assertEqual(ui.boards_with(SimpleNamespace(id=1), [self.board]), [])


class TrackerHelperTests(TestCase):
    def application(self, status, **fields):
        posting = SimpleNamespace(deadline=None, deadline_type="UNKNOWN", status="OPEN")
        values = {"posting": posting, "applied_on": None, "next_step_at": None,
                  "updated_at": timezone.now(), "task_set": related()}  # fmt: skip
        return SimpleNamespace(status=status, **{**values, **fields})

    def test_columns_and_closed(self):
        apps_ = [
            self.application(s)
            for s in ("SAVED", "SAVED", "OFFER", "REJECTED", "WITHDRAWN")
        ]
        counts = {
            c["status"]: len(c["applications"]) for c in ui.tracker_columns(apps_)
        }
        self.assertEqual(
            counts,
            {"SAVED": 2, "APPLYING": 0, "APPLIED": 0, "INTERVIEW": 0, "OFFER": 1},
        )
        self.assertEqual(len(ui.closed_applications(apps_)), 2)
        self.assertEqual(ui.active_count(apps_), 3)

    def test_application_line(self):
        applied = self.application("APPLIED", applied_on=date(2026, 10, 28))
        self.assertEqual(ui.application_line(applied), "Applied Oct 28")
        moment = datetime(
            2026,
            11,
            12,
            14,
            0,
            tzinfo=timezone.get_current_timezone(),
        )
        interview = self.application("INTERVIEW", next_step_at=moment)
        self.assertEqual(
            ui.application_line(interview), "Interview Thu, Nov 12 · 2:00 PM"
        )
        task = SimpleNamespace(title="Finish cover letter", due_at=moment, done=False)
        applying = self.application("APPLYING", task_set=related(task))
        self.assertEqual(
            ui.application_line(applying), "Finish cover letter · due Thu, Nov 12"
        )

    def test_due_this_week(self):
        now = timezone.now()
        soon = SimpleNamespace(due_at=now + timedelta(days=2), done=False)
        later = SimpleNamespace(due_at=now + timedelta(days=10), done=False)
        done = SimpleNamespace(due_at=now + timedelta(days=1), done=True)
        self.assertEqual(ui.due_this_week([later, done, soon]), [soon])


CONTRACT_NEEDS = {
    "boards.Board": ["get_absolute_url", "membership_set"],
    "boards.Membership": ["user", "role", "joined_at"],
    "postings.Posting": ["get_absolute_url"],
    "postings.BoardPosting": ["comment_set"],
    "postings.Comment": ["get_absolute_url"],
    "tracker.Application": ["get_absolute_url", "task_set"],
    "tracker.Task": ["get_absolute_url"],
}


class ContractTests(TestCase):
    """What the templates need from the real models (docs/frontend-handoff.md, section 2).

    Each check is skipped until its model exists, then has to pass.
    """

    def test_models_have_what_the_templates_read(self):
        checked = 0
        for label, attributes in CONTRACT_NEEDS.items():
            try:
                model = apps.get_model(label)
            except LookupError:
                continue
            checked += 1
            for attribute in attributes:
                with self.subTest(model=label, attribute=attribute):
                    self.assertTrue(
                        hasattr(model, attribute),
                        f"{label} needs {attribute} for the templates; see docs/frontend-handoff.md",
                    )
        if not checked:
            self.skipTest("None of these models exist yet")
