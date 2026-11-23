from django.contrib.auth import get_user_model
from django.core import serializers
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from apps.boards.models import Board, Membership

from .models import Notification
from .tasks import send_daily_digest


class NotificationViewsTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            username="student",
            email="student@example.com",
            password="test-password",
        )
        self.other_user = user_model.objects.create_user(
            username="other",
            email="other@example.com",
            password="test-password",
        )
        self.notification = Notification.objects.create(
            user=self.user,
            kind=Notification.Kind.DEADLINE_SOON,
            title="Application deadline",
            message="Your application is due soon.",
            dedupe_key="TEST:deadline",
        )

    def test_dedupe_key_is_unique_per_user(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            Notification.objects.create(
                user=self.user,
                kind=Notification.Kind.DEADLINE_SOON,
                message="Duplicate notification.",
                dedupe_key="TEST:deadline",
            )

    def test_list_renders_real_notification_fields_and_menu(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse("notifications:list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Application deadline")
        self.assertContains(response, "Your application is due soon.")
        self.assertContains(response, "2 unread")
        self.assertEqual(
            response.context["notification_menu"]["unread_count"],
            2,
        )

    def test_list_renders_the_real_signup_notification(self):
        self.client.force_login(self.user)

        response = self.client.get("/notifications/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome!")
        self.assertContains(response, "Your account has been created successfully.")
        self.assertContains(
            response,
            f'action="{reverse("notifications:open_notification")}"',
        )
        self.assertEqual(response.context["notification_menu"]["unread_count"], 2)

    def test_list_only_shows_the_signed_in_users_notifications(self):
        Notification.objects.create(
            user=self.other_user,
            kind=Notification.Kind.TASK_DUE,
            title="Private",
            message="Not yours.",
            dedupe_key="TEST:private",
        )
        self.client.force_login(self.user)

        response = self.client.get(reverse("notifications:list"))

        self.assertContains(response, "Application deadline")
        self.assertNotContains(response, "Not yours.")

    def test_mark_all_read_updates_only_the_signed_in_users_notifications(self):
        other_notification = Notification.objects.create(
            user=self.other_user,
            kind=Notification.Kind.TASK_DUE,
            title="Private",
            message="Not yours.",
            dedupe_key="TEST:private",
        )
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("notifications:mark_all_read"),
            {"next": reverse("notifications:list")},
        )

        self.notification.refresh_from_db()
        other_notification.refresh_from_db()
        self.assertTrue(self.notification.read)
        self.assertFalse(other_notification.read)
        self.assertRedirects(response, reverse("notifications:list"))

    def test_open_notification_marks_own_notification_read(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("notifications:open_notification"),
            {
                "notification": self.notification.pk,
                "next": "https://example.com/",
            },
        )

        self.notification.refresh_from_db()
        self.assertTrue(self.notification.read)
        self.assertRedirects(response, reverse("notifications:list"))

    def test_open_signup_notification_redirects_to_the_real_list(self):
        welcome_notification = Notification.objects.get(
            user=self.user,
            kind=Notification.Kind.WELCOME,
        )
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("notifications:open_notification"),
            {
                "notification": welcome_notification.pk,
                "next": "/notifications/",
            },
        )

        welcome_notification.refresh_from_db()
        self.assertTrue(welcome_notification.read)
        self.assertRedirects(response, "/notifications/")

    def test_cannot_open_another_users_notification(self):
        other_notification = Notification.objects.create(
            user=self.other_user,
            kind=Notification.Kind.TASK_DUE,
            title="Private",
            message="Not yours.",
            dedupe_key="TEST:private",
        )
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("notifications:open_notification"),
            {"notification": other_notification.pk},
        )

        self.assertEqual(response.status_code, 404)
        other_notification.refresh_from_db()
        self.assertFalse(other_notification.read)

    def test_open_notification_with_non_numeric_id_returns_404(self):
        self.client.force_login(self.user)

        for notification_id in ("abc", ""):
            with self.subTest(notification_id=notification_id):
                response = self.client.post(
                    reverse("notifications:open_notification"),
                    {"notification": notification_id},
                )
                self.assertEqual(response.status_code, 404)

    def test_notification_actions_require_authentication_and_post(self):
        response = self.client.post(reverse("notifications:mark_all_read"))
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('notifications:mark_all_read')}",
        )

        self.client.force_login(self.user)
        response = self.client.get(reverse("notifications:mark_all_read"))
        self.assertEqual(response.status_code, 405)


class NotificationTasksTests(TestCase):
    def test_daily_digest_is_a_no_op_until_email_delivery_is_implemented(self):
        user_model = get_user_model()
        active_users = [
            user_model.objects.create_user(
                username=f"active-{number}",
                email=f"active-{number}@example.com",
                password="test-password",
            )
            for number in range(2)
        ]
        user_model.objects.create_user(
            username="inactive",
            email="inactive@example.com",
            password="test-password",
            is_active=False,
        )

        notification_count = Notification.objects.count()
        created_count = send_daily_digest()
        repeat_count = send_daily_digest()

        self.assertEqual(created_count, 0)
        self.assertEqual(repeat_count, 0)
        self.assertEqual(Notification.objects.count(), notification_count)
        self.assertFalse(
            Notification.objects.filter(
                user__in=active_users,
                title="Daily digest",
            ).exists()
        )


class MembershipNotificationSignalTests(TestCase):
    def test_member_join_sends_notifications_to_member_and_board_owner(self):
        user_model = get_user_model()
        owner = user_model.objects.create_user(
            username="board-owner",
            email="owner@example.com",
            password="test-password",
        )
        member = user_model.objects.create_user(
            username="new-member",
            email="member@example.com",
            password="test-password",
        )
        board = Board.objects.create(created_by=owner, name="Study group")

        Membership.objects.create(
            board=board,
            user=owner,
            role=Membership.Role.OWNER,
        )
        membership = Membership.objects.create(
            board=board,
            user=member,
            role=Membership.Role.MEMBER,
        )

        member_notice = Notification.objects.get(
            user=member,
            dedupe_key=f"MEMBER_JOINED:{membership.pk}:JOINER",
        )
        owner_notice = Notification.objects.get(
            user=owner,
            dedupe_key=f"MEMBER_JOINED:{membership.pk}:OWNER",
        )

        self.assertIn("Study group", member_notice.message)
        self.assertIn("new-member", owner_notice.message)
        self.assertIn("Study group", owner_notice.message)
        self.assertEqual(member_notice.link_url, board.get_absolute_url())
        self.assertEqual(owner_notice.link_url, board.get_absolute_url())

    def test_owner_membership_does_not_send_member_join_notifications(self):
        user = get_user_model().objects.create_user(
            username="board-owner",
            email="owner@example.com",
            password="test-password",
        )
        board = Board.objects.create(created_by=user, name="Study group")

        membership = Membership.objects.create(
            board=board,
            user=user,
            role=Membership.Role.OWNER,
        )

        self.assertFalse(
            Notification.objects.filter(
                dedupe_key__startswith=f"MEMBER_JOINED:{membership.pk}:"
            ).exists()
        )

    def test_new_board_notification_links_to_the_board(self):
        owner = get_user_model().objects.create_user(
            username="board-owner",
            email="owner@example.com",
        )
        board = Board.objects.create(created_by=owner, name="Study group")

        notification = Notification.objects.get(
            user=owner,
            dedupe_key=f"NEW_BOARD:{board.pk}",
        )

        self.assertEqual(notification.link_url, board.get_absolute_url())


class FixtureLoadingSignalTests(TestCase):
    def test_loaddata_does_not_create_notifications(self):
        # loaddata saves each object with raw=True; the signals should skip those saves
        # (a fixture already holds whatever notifications it needs).
        now = timezone.now()  # auto_now_add doesn't run on raw saves, so set it here
        fixture = serializers.serialize(
            "json",
            [
                get_user_model()(
                    pk=901, username="fixture-owner", email="fo@example.com"
                ),
                get_user_model()(
                    pk=902, username="fixture-member", email="fm@example.com"
                ),
                Board(
                    pk=901,
                    created_by_id=901,
                    name="Fixture board",
                    join_code="FIXTURE1",
                    created_at=now,
                    updated_at=now,
                ),
                Membership(
                    pk=901,
                    board_id=901,
                    user_id=902,
                    role=Membership.Role.MEMBER,
                    joined_at=now,
                ),
            ],
        )

        for loaded in serializers.deserialize("json", fixture):
            loaded.save()  # the same save loaddata does

        self.assertEqual(Membership.objects.filter(pk=901).count(), 1)
        self.assertFalse(Notification.objects.exists())
