"""
This module contains our mapping of URL path expressions to Django views for the "accounts" application.
"""
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views

# URL namespace for this application.
app_name = 'accounts'

# URL patterns to be matched.
urlpatterns = [
    path('login/', LoginView.as_view(template_name='accounts/login.html', redirect_authenticated_user=True), name="login"),
    path('profile', views.profile, name='profile'),
    path('settings', views.settings, name='settings'),
    path('logout/', LogoutView.as_view(template_name='accounts/login.html'), name='logout'),
]
