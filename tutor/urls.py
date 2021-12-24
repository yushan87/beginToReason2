"""
This module contains our mapping of URL path expressions to Django views for the "tutor" application.
"""
from django.urls import path

from . import views

# URL namespace for this application.
app_name = 'tutor'

# URL patterns to be matched.
urlpatterns = [
    path('class/<int:classID>', views.class_view, name='class'),
    path('<int:assignmentID>', views.tutor, name='tutor'),
    path('grader', views.grader, name='grader')
]
