"""
This module contains our configuration settings for the "tutor" application.
"""
from django.apps import AppConfig


class TutorConfig(AppConfig):
    """
    The TutorConfig object stores the configuration for the "tutor" application
    """
    # Override the name of the application in AppConfig
    name = 'tutor'
