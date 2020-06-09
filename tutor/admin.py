"""
TODO: Need to fill in the correct information for this module after
      we remove experimental things that don't work.
"""
from django.contrib import admin

from .models import Lesson, Reference, CodeTemplate
from .forms import LessonForm, TemplateForm


class RefInline(admin.StackedInline):
    """
    TODO: Need to fill in the correct information for this class after
          remove experimental things that don't work.
    """
    model = Reference.lesson.through
    extra = 0
    Reference.objects.filter(reference_key=model)


class TemplateAdmin(admin.ModelAdmin):
    """
    TODO: Need to fill in the correct information for this class after
          remove experimental things that don't work.
    """
    model = CodeTemplate
    fields = ['template_name', 'template_code']
    form = TemplateForm


class ReferenceInline(admin.TabularInline):
    """
    TODO: Need to fill in the correct information for this class after
          remove experimental things that don't work.
    """
    model = Reference
    extra = 0
    fields = ['reference_key', 'reference_text']


class LessonAdmin(admin.ModelAdmin):
    """
    TODO: Need to fill in the correct information for this class after
          remove experimental things that don't work.
    """
    form = LessonForm
    inlines = [RefInline, ]

    list_filter = ['lesson_name']
    ordering = ['lesson_name']


class ReferenceAdmin(admin.ModelAdmin):
    """
    TODO: Need to fill in the correct information for this class after
          remove experimental things that don't work.
    """
    model = Reference


# Register your models here.
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Reference)
admin.site.register(CodeTemplate, TemplateAdmin)
