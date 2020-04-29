from django.contrib import admin
from django_ace import AceWidget

from .models import Lesson
from .forms import LessonForm



'''
class RefInline(admin.StackedInline):
	model = Reference.lesson.through
	extra = 0
	Reference.objects.filter(reference_key=model)

class TemplateAdmin(admin.ModelAdmin):
	model = Code_Template
	fields = ['template_name','template_code']
	form = TemplateForm

class ReferenceInline(admin.TabularInline):
	model = Reference
	extra = 0
	fields = ['reference_key','reference_text']
'''
class LessonAdmin(admin.ModelAdmin):
	form = LessonForm
#	inlines=[RefInline,]
	
	list_filter=['Name']
	ordering = ['Name']

	
'''	
class ReferenceAdmin(admin.ModelAdmin):
	model = Reference
'''


# Register your models here.
admin.site.register(Lesson,LessonAdmin)
#admin.site.register(Reference)
#admin.site.register(Code_Template,TemplateAdmin)

