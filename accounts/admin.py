"""
This module registers the models we created for the "accounts" application. After registering
the model, the data will be accessible through Django's admin functionality.
"""
from django.contrib import admin

from .models import UserInformation


# Register your models here.
admin.site.register(UserInformation)
