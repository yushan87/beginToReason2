"""
This module contains our configuration settings for the "think_aloud" application.
"""
from django.apps import AppConfig


class ThinkAloudConfig(AppConfig):
    """
    The ThinkAloudConfig object stores the configuration for the "think_aloud" application
    """
    # Override the name of the application in AppConfig
    name = 'think_aloud'
