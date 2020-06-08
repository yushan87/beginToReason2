"""
This module is a mapping between URL path expressions to Python functions (your views)
"""
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views

# URL namespace for this application.
app_name = 'accounts'

# URL patterns to be matched.
urlpatterns = [
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name="login"),
    path('profile', views.profile, name='profile'),
    path('logout/', LogoutView.as_view(template_name='accounts/login.html'), name='logout'),
]
