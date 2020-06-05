from django.urls import path
from django.conf.urls import include, url

from . import views


app_name = 'accounts'
urlpatterns = [
    path('login', views.login, name='login'),
    path('profile', views.profile, name='profile')
]