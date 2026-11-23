from celery import shared_task


@shared_task
def send_daily_digest() -> int:
    return 0
