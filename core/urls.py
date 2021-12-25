"""
This module contains our mapping of URL path expressions to Django views for the "core" application.
"""
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import path
from django.views.generic import RedirectView

from . import views

# URL namespace for this application.
app_name = 'core'

# URL patterns to be matched.
urlpatterns = [
    path('class/<int:classID>', views.class_view, name='class'),
    path('classes', views.classes, name='classes'),
    path('privacy', views.privacy, name='privacy'),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('images/favicon.ico')))
]
