"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from apps.ui_preview.views import styleguide

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", TemplateView.as_view(template_name="base.html"), name="home"),
    path("accounts/", include("apps.accounts.urls")),
    path("boards/", include("apps.boards.urls")),
    path("postings/", include("apps.postings.urls")),
    path("tracker/", include("apps.tracker.urls")),
    path("notifications/", include("apps.notifications.urls")),
    path("ingestion/", include("apps.ingestion.urls")),
]

# Every UI component on one page, for copying markup. Development only.
if settings.DEBUG:
    urlpatterns += [path("styleguide/", styleguide, name="styleguide")]
