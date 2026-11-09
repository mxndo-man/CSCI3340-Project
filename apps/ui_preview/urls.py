"""The preview pages, at /preview/ only when UI_PREVIEW is on (see config/urls.py).

Each path is the real path from docs/contracts.md section 7, under /preview/.
"""

from django.urls import path

from . import views

app_name = "ui_preview"

urlpatterns = [
    path("", views.index, name="index"),
    path("action/", views.action, name="action"),
    path("postings/", views.discover, name="discover"),
    path("postings/add/", views.posting_add, name="posting_add"),
    path("postings/<int:pk>/", views.posting_detail, name="posting_detail"),
    path("boards/", views.boards, name="boards"),
    path("boards/<int:pk>/", views.board_detail, name="board_detail"),
]
