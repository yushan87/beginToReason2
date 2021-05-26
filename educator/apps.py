"""
This module contains our configuration settings for the "educator" application.
"""
from django.apps import AppConfig


class EducatorConfig(AppConfig):
    """
        The CoreConfig object stores the configuration for the "educator" application
    """
    # Override the name of the application in AppConfig
    name = 'educator'
