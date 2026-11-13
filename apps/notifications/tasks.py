from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import Notifications


@shared_task
def send_daily_digest() -> int:
    today = timezone.localdate()
    already_notified = Notifications.objects.filter(
        title="Daily digest",
        created_at__date=today,
    ).values_list("recipient_id", flat=True)
    recipient_ids = (
        get_user_model()
        .objects.filter(is_active=True)
        .exclude(pk__in=already_notified)
        .values_list("pk", flat=True)
    )
    notifications = [
        Notifications(
            recipient_id=recipient_id,
            title="Daily digest",
            message="Check your dashboard for new opportunities and upcoming deadlines.",
        )
        for recipient_id in recipient_ids
    ]
    return len(Notifications.objects.bulk_create(notifications))