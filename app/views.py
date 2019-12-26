from django.shortcuts import render
from django.http import HttpResponse

from django.views.generic.edit import FormView
from django.urls import reverse


# Create your views here.

def index(request):
	return HttpResponse("app")