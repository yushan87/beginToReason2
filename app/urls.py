from django.urls import path
from django.conf.urls import include, url

from . import views


app_name = 'app'
urlpatterns = [
    path('', views.index, name='index'),
    path('lesson', views.lesson, name='lesson'),
    path('testPage', views.testPage, name='testPage'),
]