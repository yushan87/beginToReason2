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

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Media files (User-uploaded files)
# https://docs.djangoproject.com/en/3.2/ref/settings/#std:setting-MEDIA_ROOT
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

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
