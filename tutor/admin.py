"""
TODO: Need to fill in the correct information for this module after
      we remove experimental things that don't work.
"""
from django.contrib import admin

from .models import Lesson, Reference, CodeTemplate, Instruction, Reasoning, MC_Choice, Question, Free_Resp
from .forms import LessonForm, TemplateForm

'''
class RefInline(admin.StackedInline):
    """
    TODO: Need to fill in the correct information for this class after
          remove experimental things that don't work.
    """
    model = Reference.lesson.through
    extra = 0
    Reference.objects.filter(reference_key=model)

'''
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

    list_filter = ['lesson_name']
    ordering = ['lesson_name']


class ReferenceAdmin(admin.ModelAdmin):
    """
    TODO: Need to fill in the correct information for this class after
          remove experimental things that don't work.
    """
    model = Reference





# Register your models here.
admin.site.register(Lesson)
admin.site.register(Reference)
admin.site.register(CodeTemplate)
admin.site.register(Instruction)
admin.site.register(Reasoning)
admin.site.register(Question)
admin.site.register(MC_Choice)
admin.site.register(Free_Resp)
