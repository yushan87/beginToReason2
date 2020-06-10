"""
This module is a mapping between URL path expressions to Python functions (your views)
"""
from django.apps import AppConfig


class BegintoReasonConfig(AppConfig):
    """
    The BeginToReasonConfig object stores the configuration for the BeginToReason sub-application.
    """
    # Override the name of the application in AppConfig
    name = 'app'
