"""
This module contains our Django views for the "data_analysis" application.
"""
from django.shortcuts import render
from data_analysis.py_helper_functions.graph_viewer.lesson_reader import lesson_to_json, lesson_stats
# Create your views here.
def d3Graph(request, index):
    print(request)
    return render(request, "data_analysis/d3graph.html", {'graphData': lesson_to_json(index), 'lessonData': lesson_stats(index)})