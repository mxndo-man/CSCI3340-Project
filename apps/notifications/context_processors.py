from .models import Notification


def notification_menu(request):
    if not request.user.is_authenticated:
        return {}

    notifications = Notification.objects.filter(user=request.user)
    return {
        "notification_menu": {
            "notifications": notifications[:5],
            "unread_count": notifications.filter(read=False).count(),
        }
    }
