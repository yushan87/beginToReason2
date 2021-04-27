"""
This module contains our mapping of URL path expressions to Django views for the "educator" application.
"""
from django.urls import path
from . import views

# URL namespace for this application.
app_name = 'educator'

# URL patterns to be matched.
urlpatterns = [
    path('create_class', views.create_class, name='create_class'),
    path('instructor', views.instructor, name='instructor'),

]
