"""
This module contains our mapping of URL path expressions to Django views for the "instructor" application.
"""
from django.urls import path

from . import views

# URL namespace for this application.
app_name = 'instructor'

# URL patterns to be matched.
urlpatterns = [
    path('', views.instructor, name='main-view'),
    path('class/<int:classID>', views.class_view_instructor, name='class-view'),
    path('editAssignment', views.edit_assignment, name='edit-assignment')
]
