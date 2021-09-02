"""
Django production settings for begintoreason_django project.

This file contains the settings that are only used in
production mode.
"""

from .base import *

# Turn off debug mode
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# In production mode, we need to provide the qualified domain
# we are hosting this application.
ALLOWED_HOSTS = []
