from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    RedirectURLMixin,  # pyright: ignore[reportAttributeAccessIssue]
)
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView

from .models import Notification


class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = "notifications/list.html"
    context_object_name = "notifications"

    def get_queryset(self):
        return Notification.objects.filter(user_id=self.request.user.pk)


class MarkAllReadView(LoginRequiredMixin, RedirectURLMixin, View):
    def post(self, request: HttpRequest):
        Notification.objects.filter(
            user_id=request.user.pk,
            read=False,
        ).update(read=True)
        return redirect(self.get_redirect_url() or reverse("notifications:list"))


class OpenNotificationView(LoginRequiredMixin, RedirectURLMixin, View):
    def post(self, request: HttpRequest):
        notification = get_object_or_404(
            Notification,
            pk=request.POST.get("notification"),
            user_id=request.user.pk,
        )
        notification.read = True
        notification.save(update_fields=["read"])
        return redirect(self.get_redirect_url() or reverse("notifications:list"))
