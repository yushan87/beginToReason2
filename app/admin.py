from django.contrib import admin
from django_ace import AceWidget

from .models import Lesson, Reference, CodeTemplate
from .forms import LessonForm, TemplateForm


class RefInline(admin.StackedInline):
    model = Reference.lesson.through
    extra = 0
    Reference.objects.filter(reference_key=model)


class TemplateAdmin(admin.ModelAdmin):
    model = CodeTemplate
    fields = ['template_name', 'template_code']
    form = TemplateForm


class ReferenceInline(admin.TabularInline):
    model = Reference
    extra = 0
    fields = ['reference_key', 'reference_text']


class LessonAdmin(admin.ModelAdmin):
    form = LessonForm
    inlines = [RefInline, ]

    list_filter = ['lesson_name']
    ordering = ['lesson_name']


class ReferenceAdmin(admin.ModelAdmin):
    model = Reference


# Register your models here.
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Reference)
admin.site.register(CodeTemplate, TemplateAdmin)
