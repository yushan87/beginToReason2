"""
This module registers the models we created for the "instructor" application. After registering
the model, the data will be accessible through Django's admin functionality.
"""
from django.contrib import admin
from .models import Class

admin.site.register(Class)
