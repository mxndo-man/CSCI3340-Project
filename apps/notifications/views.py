from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    RedirectURLMixin,  # pyright: ignore[reportAttributeAccessIssue]
)
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView

from .models import Notifications


class NotificationListView(LoginRequiredMixin, ListView):
    model = Notifications
    template_name = "notifications/list.html"
    context_object_name = "notifications"

    def get_queryset(self):
        return Notifications.objects.filter(recipient_id=self.request.user.pk)


class MarkAllReadView(LoginRequiredMixin, RedirectURLMixin, View):
    def post(self, request: HttpRequest):
        Notifications.objects.filter(
            recipient_id=request.user.pk,
            is_read=False,
        ).update(is_read=True)
        return redirect(self.get_redirect_url() or reverse("notifications:list"))


class OpenNotificationView(LoginRequiredMixin, RedirectURLMixin, View):
    def post(self, request: HttpRequest):
        notification = get_object_or_404(
            Notifications,
            pk=request.POST.get("notification"),
            recipient_id=request.user.pk,
        )
        notification.is_read = True
        notification.save(update_fields=["is_read"])
        return redirect(self.get_redirect_url() or reverse("notifications:list"))
