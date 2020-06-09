"""
This module contains our configuration settings for the "data_analysis" application.
"""
from django.apps import AppConfig


class DataAnalysisConfig(AppConfig):
    """
    The ThinkAloudConfig object stores the configuration for the "data_analysis" application
    """
    # Override the name of the application in AppConfig
    name = 'data_analysis'
