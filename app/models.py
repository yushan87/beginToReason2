from django.db import models
from django import forms
from django_ace import AceWidget


# Create your models here.

class Code_Template(models.Model):
	template_name = models.CharField(max_length=30)
	template_code = models.TextField(max_length=500)

	def __str__(self):
		return self.template_name

class Lesson(models.Model):
	Name = models.CharField(max_length=30)
	Concept = models.CharField(max_length=50)
	Code = models.TextField(max_length=500)
	Activity = models.TextField(max_length=500)
	References = models.TextField(max_length=500)

	def __str__(self):
		return self.Name

class Reference(models.Model):
	reference_key = models.CharField(max_length=30)
	reference_text = models.TextField(max_length=250)
	lesson = models.ManyToManyField(Lesson, related_name='references')#, through= 'LessonReferences')
	
	def __str__(self):
		return self.reference_key		





'''
class LessonForm(forms.Form):
	class Meta:
		model = Reference.lesson.through
		widgets = forms.ManyToManyRawIdWidget()
		fields = '__all__'
		
class LessonReferences(models.Model):
	class Meta:
		order_with_respect_to = 'ref'
		unique_together = [
			('ref','lesson'),
		]
	
	ref = models.ForeignKey(Reference, models.CASCADE)
	lesson = models.ForeignKey(Lesson, models.CASCADE)
'''

