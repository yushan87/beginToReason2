"""
This module is a mapping between URL path expressions to Python functions (your views)
"""
from django.urls import path

from . import views

# URL namespace for this application.
app_name = 'app'

# URL patterns to be matched.
urlpatterns = [
    path('', views.home, name='home'),
    path('tutor', views.tutor, name='tutor'),
]
