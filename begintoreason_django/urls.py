"""begintoreason_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os
from django.contrib import admin
from django.urls import include, path
from core import views

urlpatterns = [
    # Our own applications
    path('', views.home, name='index'),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('core/', include('core.urls', namespace='core')),
    path('data_analysis/', include('data_analysis.urls', namespace='data_analysis')),
    path('educator/', include('educator.urls', namespace='educator')),
    path('think_aloud/', include('think_aloud.urls', namespace='think_aloud')),
    path('tutor/', include('tutor.urls', namespace='tutor')),

    # Django admin
    path(os.getenv('SECRET_ADMIN_URL') + 'admin/', admin.site.urls),

    # External Plugins
    path('', include('social_django.urls', namespace='social'))
]
