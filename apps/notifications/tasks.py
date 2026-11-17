from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import Notification


@shared_task
def send_daily_digest() -> int:
    today = timezone.localdate()
    dedupe_key = f"DIGEST:{today.isoformat()}"
    already_notified = Notification.objects.filter(
        dedupe_key=dedupe_key,
    ).values_list("user_id", flat=True)
    recipient_ids = (
        get_user_model()
        .objects.filter(is_active=True)
        .exclude(pk__in=already_notified)
        .values_list("pk", flat=True)
    )
    notifications = [
        Notification(
            user_id=recipient_id,
            kind=Notification.Kind.NEW_MATCH,
            title="Daily digest",
            message="Check your dashboard for new opportunities and upcoming deadlines.",
            dedupe_key=dedupe_key,
        )
        for recipient_id in recipient_ids
    ]
    return len(Notification.objects.bulk_create(notifications))
