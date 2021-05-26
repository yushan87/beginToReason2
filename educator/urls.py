"""
This module contains our mapping of URL path expressions to Django views for the "educator" application.
"""
from django.urls import path

from . import views

# URL namespace for this application.
app_name = 'educator'

# URL patterns to be matched.
urlpatterns = [
    path('', views.educator, name='main-view'),
    path('class/<int:classID>', views.class_view_educator, name='class-view'),
    path('members/<int:classID>', views.members, name='members'),
    path('editAssignment', views.edit_assignment, name='edit-assignment'),
    path('editClass', views.edit_class, name='edit-class'),
    path('promoteStudent', views.promote_student, name='promote-student')
]
