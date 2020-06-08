"""
This module is a mapping between URL path expressions to Python functions (your views)
"""
from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """
    The AccountsConfig object stores the configuration for the Accounts sub-application.
    """
    name = 'accounts'
