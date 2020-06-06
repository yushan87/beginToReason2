from django.urls import path
from django.conf.urls import include, url
from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView

from . import views


app_name = 'accounts'
urlpatterns = [
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name="login"),
    path('profile', views.profile, name='profile'),
    path('logout/', LogoutView, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),

]
