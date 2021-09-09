"""
Django base settings for begintoreason_django project.

This file contains the settings that are shared in development
and production modes. See `development.py` and `production.py`
for specific settings. See
https://www.digitalocean.com/community/tutorials/how-to-harden-your-production-django-project
for how we split these into separate files.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os

# Create a base directory variable so that we can use it
# inside the project like this: os.path.join(BASE_DIR, ...)
# NOTE: We are several levels deep, so we need to back up a bit.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ID for the current application in the django_site database.
# https://docs.djangoproject.com/en/3.2/ref/settings/#site-id
SITE_ID = 1

# Location for the root URLconf
# https://docs.djangoproject.com/en/3.2/ref/settings/#root-urlconf
ROOT_URLCONF = 'begintoreason_django.urls'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Path to the WSGI application object for Django's built-in servers will use
# https://docs.djangoproject.com/en/3.2/ref/settings/#wsgi-application
WSGI_APPLICATION = 'begintoreason_django.wsgi.application'

# Load the secret key from our .env file
# SECURITY WARNING: keep the secret key used in production secret!
# https://docs.djangoproject.com/en/3.2/ref/settings/#secret-key
SECRET_KEY = os.getenv('SECRET_KEY')

# A list of installed application and plugins we will be
# using in our application.
# https://docs.djangoproject.com/en/3.2/ref/settings/#installed-apps
INSTALLED_APPS = [
    # Django Applications
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # Our own applications
    'accounts',
    'core',
    'data_analysis',
    'educator',
    'think_aloud',
    'tutor',

    # External Plugins
    'social_django',
    'django_ace',
    'compressor',
    'crispy_forms',
    'mathfilters'
]

# A framework of hooks into Django's request/response processing
# https://docs.djangoproject.com/en/3.2/topics/http/middleware/
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Template Engine
# https://docs.djangoproject.com/en/3.2/ref/settings/#templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Authentication backends
# https://docs.djangoproject.com/en/3.2/topics/auth/customizing/#authentication-backends
AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin
    'django.contrib.auth.backends.ModelBackend',

    # Google OAuth2
    'social_core.backends.google.GoogleOAuth2',
]

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Login URL, Redirect URL and Logout URL
# https://docs.djangoproject.com/en/3.2/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = '/'   # The requests are redirected after login when the LoginView doesn't get a `next` parameter
LOGOUT_REDIRECT_URL = '/'  # The requests are redirected after logout if LogoutView doesn't have a `next_page` attribute

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'EST'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# django-compressor
# https://django-compressor.readthedocs.io/en/stable/
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',

    # other finders..
    'compressor.finders.CompressorFinder'
]

# Django 3.2 introduced a customization of primary keys. Since I don't believe that's a priority at the moment,
# this setting makes all unset primary keys default to what replaced the only option before (i.e. no change)
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# django-crispy-forms
# https://django-crispy-forms.readthedocs.io/en/latest/
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# django-libsass
# https://github.com/torchbox/django-libsass
COMPRESS_PRECOMPILERS = [
    ('text/x-scss', 'django_libsass.SassCompiler')
]

# python-social-auth
# https://python-social-auth.readthedocs.io/en/latest/
SOCIAL_AUTH_URL_NAMESPACE = 'social'

# Load the client keys and secret for Google OAuth2
# SECURITY WARNING: keep these private!
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')
