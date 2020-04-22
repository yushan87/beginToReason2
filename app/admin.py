from django.contrib import admin
from django_ace import AceWidget

from .models import Lesson
from .forms import LessonForm



class LessonAdmin(admin.ModelAdmin):
	form = LessonForm

	list_filter=['Name']
	ordering = ['Name']



# Register your models here.
admin.site.register(Lesson,LessonAdmin)