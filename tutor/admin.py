"""
This module registers the models we created for the "tutor" application. After registering
the model, the data will be accessible through Django's admin functionality.
"""
from django.contrib import admin
from tutor.models import LessonLog

# Register your models here.
admin.site.register(LessonLog)
