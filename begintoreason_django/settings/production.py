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
ALLOWED_HOSTS = [os.getenv('ALLOWED_HOSTS')]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.getenv('STATIC_ROOT')

# Media files (User-uploaded files)
# https://docs.djangoproject.com/en/3.2/ref/settings/#std:setting-MEDIA_ROOT
MEDIA_URL = '/media/'
MEDIA_ROOT = os.getenv('MEDIA_ROOT')

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases#
#
# We are temporarily using SQLite, but we should switch to something
# that is more for production mode.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# SSL Redirect
# https://docs.djangoproject.com/en/3.2/ref/settings/#secure-ssl-redirect
#
# Redirect all non-HTTPS requests to HTTPS
SECURE_SSL_REDIRECT = True

# X-XSS-Protection
# https://docs.djangoproject.com/en/3.2/ref/settings/#secure-browser-xss-filter
#
# Enable X-XSS-Protection for HTTP header on old browsers.
SECURE_BROWSER_XSS_FILTER = True

# HTTP Strict Transport Security
# https://docs.djangoproject.com/en/3.2/ref/settings/#secure-hsts-include-subdomains
# https://docs.djangoproject.com/en/3.2/ref/settings/#secure-hsts-preload
# https://docs.djangoproject.com/en/3.2/ref/settings/#secure-hsts-seconds
# https://docs.djangoproject.com/en/3.2/ref/middleware/#http-strict-transport-security
#
# Reduces your exposure to some SSL-stripping man-in-the-middle (MITM) attacks.
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_SECONDS = 31536000

# Secure Session Cookie
# https://docs.djangoproject.com/en/3.2/ref/settings/#session-cookie-secure
#
# Use a secure cookie for the session cookie, so that browsers may ensure it
# is only sent with an HTTPS connection.
SESSION_COOKIE_SECURE = True

# Secure CSRF Cookie
# https://docs.djangoproject.com/en/3.2/ref/settings/#csrf-cookie-secure
#
# Use a secure cookie for the CSRF cookie, so that browsers may ensure it
# is only sent with an HTTPS connection.
CSRF_COOKIE_SECURE = True

# python-social-auth
# https://python-social-auth.readthedocs.io/en/latest/
#
# Use HTTPS to create redirect URIs.
SOCIAL_AUTH_REDIRECT_IS_HTTPS = True
