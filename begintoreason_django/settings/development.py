"""
Django development settings for begintoreason_django project.

This file contains the settings that are only used in
development mode.
"""

from .base import *

# Turn on debug mode
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# In debug mode, subdomains of `localhost` are allowed.
ALLOWED_HOSTS = []
