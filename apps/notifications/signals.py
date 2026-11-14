from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.accounts.models import CustomUser

from .models import Notifications


@receiver(post_save, sender=CustomUser)
def create_welcome_notification(sender, instance, created, **kwargs):
    if not created:
        return

    Notifications.objects.create(
        recipient=instance,
        title="Welcome!",
        message="Your account has been created successfully. Make connections and find oppurtunities!",
    )
