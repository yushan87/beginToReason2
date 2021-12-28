"""
This module contains our configuration settings for the "parsons" application.
"""
from django.apps import AppConfig


class ParsonsConfig(AppConfig):
    """
    The ParsonsConfig object stores the configuration for the "parsons" application
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'parsons'
