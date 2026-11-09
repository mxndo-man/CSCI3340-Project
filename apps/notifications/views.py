from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .models import Notifications


class NotificationListView(LoginRequiredMixin, ListView):
	model = Notifications
	template_name = "notifications/list.html"
	context_object_name = "notifications"

	def get_queryset(self):
		return self.request.user.notifications.all()
