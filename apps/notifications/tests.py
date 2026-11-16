from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

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
    def test_daily_digest_notifies_active_users_only_once_per_day(self):
        user_model = get_user_model()
        active_users = [
            user_model.objects.create_user(
                username=f"active-{number}",
                email=f"active-{number}@example.com",
                password="test-password",
            )
            for number in range(2)
        ]
        inactive_user = user_model.objects.create_user(
            username="inactive",
            email="inactive@example.com",
            password="test-password",
            is_active=False,
        )

        created_count = send_daily_digest()
        repeat_count = send_daily_digest()

        self.assertEqual(created_count, 2)
        self.assertEqual(repeat_count, 0)
        self.assertEqual(
            Notification.objects.filter(
                dedupe_key=f"DIGEST:{timezone.localdate().isoformat()}",
                title="Daily digest",
            ).count(),
            len(active_users),
        )
        self.assertFalse(
            Notification.objects.filter(
                user=inactive_user,
                title="Daily digest",
            ).exists()
        )
