# This is the instance of celery.py

import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")

app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
app.conf.beat_schedule = {
    "add-every-6-hours": {
        "task": "tasks.add",
        "schedule": crontab(minute=0, hour="*/6"),
    },
    "daily-diget": {
        "task": "app.notificatinos.tasks.send_daily_digest",
        "schedule": crontab(minute=0, hour=8),
    },
}
