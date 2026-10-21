from celery import shared_task

@shared_task
def sync_sources():
    """TODO: ingestion of 6 hours"""