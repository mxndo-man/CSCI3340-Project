from django.urls import path

from . import views

app_name = "accounts"
urlpatterns: list = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
]
