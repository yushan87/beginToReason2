"""
This module contains our configuration settings for the "instructor" application.
"""
from django.apps import AppConfig


class InstructorConfig(AppConfig):
    """
        The CoreConfig object stores the configuration for the "instructor" application
    """
    # Override the name of the application in AppConfig
    name = 'instructor'
