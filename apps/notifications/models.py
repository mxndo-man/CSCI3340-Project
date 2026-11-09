# Create your models here.
from django.db import models
from django.conf import settings

class Notifications(models.Model):
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            # 1. Speeds up the default chronological ordering
            models.Index(fields=['-created_at']),
            
            # 2. Speeds up fetching a specific user's  notifications
            models.Index(fields=['recipient', '-created_at']),
            
            # 3. unread/recent
            models.Index(fields=["recipient", "is_read", "-created_at"]),
        ]