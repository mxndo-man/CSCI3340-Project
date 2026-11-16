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
    "daily-digest": {
        "task": "apps.notifications.tasks.send_daily_digest",
        "schedule": crontab(minute=0, hour=8), # Creates daily digest to all users at 8am Chicago Time
    },
}
