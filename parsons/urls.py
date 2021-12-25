"""
This module contains our mapping of URL path expressions to Django views for the "tutor" application.
"""
from django.urls import path
from . import views

# URL namespace for this application.
app_name = 'parsons'

# URL patterns to be matched.
urlpatterns = [
    path('parsons/<int:assignmentID>', views.parsons_problem, name='parsons'),
    path('parsonsAdvance/<int:assignmentID>', views.advance_parsons_lesson, name='parsonsAdvance'),
]
