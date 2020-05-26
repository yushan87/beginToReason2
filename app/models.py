from django.db import models
from django import forms
from django_ace import AceWidget
from django.contrib.auth.models import (
	BaseUserManager, AbstractBaseUser
)


# Create your models here.

class Code_Template(models.Model):
	template_name = models.CharField(max_length=30)
	template_code = models.TextField(max_length=500)

	def __str__(self):
		return self.template_name

class Lesson(models.Model):
	lesson_name = models.CharField(max_length=30)
	lesson_code = models.TextField(max_length=500)
	template = Code_Template

	def __str__(self):
		return self.lesson_name

class Reference(models.Model):
	reference_key = models.CharField(max_length=30)
	reference_text = models.TextField(max_length=250)
	lesson = models.ManyToManyField(Lesson, related_name='references')#, through= 'LessonReferences')
	
	def __str__(self):
		return self.reference_key		

class UserInformation(models.Model):
	user_email = models.EmailField(max_length=320)
	user_id = models.IntegerField(max_length=30)
	user_name = models.TextField(max_length=30)

	def __str__(self):
		return self.user_id

	@classmethod
	def create(cls, email, name):
		user = cls(email=email)
		user = cls(name=name)
		# do something with the book
		return user




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

