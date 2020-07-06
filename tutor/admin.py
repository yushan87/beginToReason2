"""
TODO: Need to fill in the correct information for this module after
      we remove experimental things that don't work.
"""
from django.contrib import admin

from .models import Lesson, Reference, Reasoning, McChoice, Question, Code


# Register your models here.
admin.site.register(Lesson)
admin.site.register(Code)
admin.site.register(Reference)
admin.site.register(Reasoning)
admin.site.register(Question)
admin.site.register(McChoice)

