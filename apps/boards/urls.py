from django.urls import path
from . import views


app_name = "boards"
urlpatterns: list = [
    path("", views.board_list_view, name="list"),
    path("join/", views.join_board_view, name="join"),
    path("new/", views.create_board_view, name="create"),
    path("<int:pk>/", views.board_detail_view, name="detail"),
    path("<int:board_id>/leave/", views.leave_board_view, name="leave"),
    path(
        "<int:board_id>/remove/<int:user_id>/", views.remove_member_view, name="remove"
    ),
]
