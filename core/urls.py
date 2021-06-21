"""
This module contains our mapping of URL path expressions to Django views for the "core" application.
"""
from django.urls import path

from . import views

# URL namespace for this application.
app_name = 'core'

# URL patterns to be matched.
urlpatterns = [
    path('privacy', views.privacy, name='privacy')
]
