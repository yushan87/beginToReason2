"""
This module contains our mapping of URL path expressions to Django views for the "data_analysis" application.
"""
from django.urls import path

from . import views

# URL namespace for this application.
app_name = 'data_analysis'

# URL patterns to be matched.
urlpatterns = [
    path('d3Graph/<int:index>', views.d3Graph, name="d3Graph")
    path('instructor', views.instructor, name='instructor')
]
