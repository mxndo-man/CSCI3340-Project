from .models import Notifications


def notification_menu(request):
    if not request.user.is_authenticated:
        return {}

    notifications = Notifications.objects.filter(recipient=request.user)
    return {
        "notification_menu": {
            "notifications": notifications[:5],
            "unread_count": notifications.filter(is_read=False).count(),
        }
    }
