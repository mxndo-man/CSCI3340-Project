from celery import shared_task

@shared_task
def send_daily_digest():
    """TODO: notifications daily ingest"""