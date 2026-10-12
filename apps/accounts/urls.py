# apps/accounts/urls.py
from django.urls import path
from .views import register_view, test_page_view, logout_view

urlpatterns = [
    path('register/', register_view, name='register'),
    path('test-page/', test_page_view, name='test_page'),
    path('logout/', logout_view, name='logout'),
]
