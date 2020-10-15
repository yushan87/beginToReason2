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
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name="login"),
<<<<<<< HEAD
    path('profile/', views.profile, name='profile'),
    path('settings/', views.settings, name='settings'),
=======
    path('profile', views.profile, name='profile'),
    path('settings', views.settings, name='settings'),
    path('privacy', views.privacy, name='privacy'),
>>>>>>> 87077fa160c41422b2839aa2302f973bab8f92f9
    path('logout/', LogoutView.as_view(template_name='accounts/login.html'), name='logout'),
]
