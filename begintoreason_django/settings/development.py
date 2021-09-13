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

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
#
# We will be using SQLite for development mode.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
