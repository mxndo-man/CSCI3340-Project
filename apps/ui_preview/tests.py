"""Tests for the preview: every page renders with UI_PREVIEW on, on the logged-in account,
and none exist with it off."""

from django.test import TestCase, override_settings
from django.urls import reverse

from apps.ui.templatetags import ui
from apps.ui.tests import DEV, LIVE, make_user, status_of

from . import filters
from .views import INDEX_PAGES

# Every preview page, plus the logged-out versions of a few.
PAGES = ["/preview/"] + [
    reverse(name, args=args, urlconf=DEV) for _, name, args, _ in INDEX_PAGES
]
VISITOR_PAGES = ["/preview/postings/?as=visitor", "/preview/postings/1/?as=visitor"]
# The pages anyone can see, as in the prototype; every other one needs an account.
PUBLIC_PAGES = ["/preview/", "/preview/postings/"] + [
    path
    for path in PAGES
    if path.startswith("/preview/postings/") and path[-2].isdigit()
]
ACCOUNT_PAGES = [path for path in PAGES if path not in PUBLIC_PAGES]


@override_settings(ROOT_URLCONF=DEV)
class PreviewOnTests(TestCase):
    def setUp(self):
        # id 2 was the fake Maya K.'s id once; it checks no fake person is taken for "you".
        self.user = make_user(id=2, display_name="Quinn A.", username="quinn")
        self.client.force_login(self.user)

    def test_every_page_renders(self):
        for path in PAGES + VISITOR_PAGES:
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(status_of(response), 200)
                self.assertContains(response, "Preview:")  # the banner

    def test_the_preview_is_on_your_account(self):
        response = self.client.get("/preview/boards/1/")
        self.assertContains(response, "Quinn A. (you)")  # in the Members dialog
        self.assertNotContains(response, "Liam R.")
        home = self.client.get("/preview/home/")
        self.assertContains(home, ", Quinn</h1>")  # "Good morning, Quinn"

    def test_only_you_are_you(self):
        # Board 1's first posting has a comment by you and one by Maya K.
        response = self.client.get("/preview/boards/1/")
        self.assertContains(
            response, '<span class="font-semibold text-bark-900">You</span>'
        )
        self.assertContains(
            response, '<span class="font-semibold text-bark-900">Maya K.</span>'
        )

    def test_every_stand_in_exists(self):
        for name, stand_in in ui.PREVIEW_PAGES.items():
            with self.subTest(name=name):
                self.assertTrue(reverse(stand_in))

    def test_forms_say_nothing_was_saved(self):
        response = self.client.post(
            "/preview/action/", {"next": "/preview/boards/"}, follow=True
        )
        self.assertRedirects(response, "/preview/boards/")
        self.assertContains(response, "Preview only, nothing was saved")

    def test_action_wont_redirect_off_site(self):
        response = self.client.post(
            "/preview/action/", {"next": "https://evil.example/"}
        )
        self.assertRedirects(response, "/preview/")

    def test_board_roles(self):
        # You own board 1 and are only a member of board 3.
        owned = self.client.get("/preview/boards/1/")
        self.assertContains(owned, "Remove<span")
        self.assertNotContains(owned, "Leave board")
        member = self.client.get("/preview/boards/3/")
        self.assertContains(member, "Leave board")
        self.assertNotContains(member, "Remove<span")

    def test_board_forms_show_errors(self):
        response = self.client.post("/preview/boards/join/", {"join_code": ""})
        self.assertEqual(status_of(response), 200)
        self.assertContains(response, "This field is required")


@override_settings(ROOT_URLCONF=DEV)
class PreviewLoggedOutTests(TestCase):
    def test_account_pages_ask_you_to_log_in(self):
        for path in ACCOUNT_PAGES:
            with self.subTest(path=path):
                self.assertRedirects(
                    self.client.get(path),
                    f"/accounts/login/?next={path}",
                    fetch_redirect_response=False,
                )

    def test_public_pages_show_the_logged_out_version(self):
        for path in PUBLIC_PAGES:
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertContains(response, "seen logged out")
                self.assertNotContains(response, "Account menu")


@override_settings(ROOT_URLCONF=LIVE)
class PreviewOffTests(TestCase):
    def test_no_preview_pages(self):
        for path in PAGES + ["/preview/action/"]:
            with self.subTest(path=path):
                self.assertEqual(status_of(self.client.get(path)), 404)


class FilterTests(TestCase):
    def test_a_saved_search_link_reads_back_as_the_same_filters(self):
        saved = {
            "paid": True,
            "clearance": ["NONE_MENTIONED"],
            "deadline_within_days": 30,
        }
        query = ui.discover_query(saved)
        params = dict(pair.split("=") for pair in query.split("&"))
        parsed = filters.parse_filters(params)
        self.assertEqual(filters.compact(parsed), saved)
