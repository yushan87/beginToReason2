"""
This file generates the admin db tables related to accounts
"""
from django.contrib import admin

from .models import UserInformation


# Register your models here.
admin.site.register(UserInformation)
