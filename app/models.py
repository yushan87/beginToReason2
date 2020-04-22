from django.db import models
from django import forms
from django_ace import AceWidget


# Create your models here.


class Lesson(models.Model):
	Name = models.CharField(max_length=30)
	Concept = models.CharField(max_length=50)
	Code = models.TextField(max_length=500)
	Activity = models.TextField(max_length=500)
	References = models.TextField(max_length=500)

	def __str__(self):
		return self.Name

