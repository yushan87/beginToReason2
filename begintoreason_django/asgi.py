"""
ASGI config for begintoreason_django project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
import dotenv

from django.core.asgi import get_asgi_application

dotenv.load_dotenv(
    os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'begintoreason_django.settings.development')

if os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = os.getenv('DJANGO_SETTINGS_MODULE')

application = get_asgi_application()
