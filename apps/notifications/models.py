from django.conf import settings
from django.db import models


class Notification(models.Model):
    class Kind(models.TextChoices):
        TASK_DUE = "TASK_DUE", "Task due"
        DEADLINE_SOON = "DEADLINE_SOON", "Deadline soon"
        NEW_MATCH = "NEW_MATCH", "New match"
        POSTING_CLOSED = "POSTING_CLOSED", "Posting closed"
        WELCOME = "WELCOME", "Welcome"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    kind = models.CharField(max_length=20, choices=Kind.choices)
    title = models.CharField(max_length=255, blank=True)
    message = models.CharField(max_length=300)
    link_url = models.CharField(max_length=300, blank=True)
    dedupe_key = models.CharField(max_length=200)
    read = models.BooleanField(default=False)
    emailed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
        indexes = (
            models.Index(fields=["-created_at"]),
            models.Index(fields=["user", "-created_at"]),
            models.Index(fields=["user", "read", "-created_at"]),
        )
        constraints = (
            models.UniqueConstraint(
                fields=("user", "dedupe_key"),
                name="notif_user_dedupe_uniq",
            ),
        )

