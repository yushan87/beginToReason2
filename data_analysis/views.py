"""
This module contains our Django views for the "data_analysis" application.
"""
from django.shortcuts import render
from data_analysis.py_helper_functions.graph_viewer.lesson_reader import read_lesson
# Create your views here.
def dummyGraph(request):
    """function catalog This function handles the view for the dummyGraph page of the application.
        Args:
            request (HTTPRequest): A http request object created automatically by Django.
        Returns:
            HttpResponse: A generated http response object to the request
        """
    print(request)
    return render(request, "data_analysis/dummyGraph.html", {'imgSrc': read_lesson(13)
    })