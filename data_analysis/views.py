"""
This module contains our Django views for the "data_analysis" application.
"""
from django.shortcuts import render
from data_analysis.py_helper_functions.lesson_stats import get_set_stats, get_set_info
from data_analysis.py_helper_functions.graph_viewer.lesson_reader import lesson_to_json, lesson_info


# Create your views here.
def d3_graph(request, setID, lessonIndex):
    """function d3_graph This function handles the view for the graph of a specific lesson

    Args:
        request (HTTPRequest): A http request object created automatically by Django.
        setID (int): ID of the set within the database
        lessonIndex (int): index of the lesson within the set's lessons() call

    Returns:
        HttpResponse: A generated http response object to the request to generate the graph
    """
    print(request)
    return render(request, "data_analysis/d3graph.html", {'graphData': lesson_to_json(setID, lessonIndex, True),
                                                          'lessonData': lesson_info(setID, lessonIndex)})


def set_statistics(request, setID):
    """function d3_graph This function handles the view for lesson set-wide stats

    Args:
        request (HTTPRequest): A http request object created automatically by Django.
        setID (int): ID of the set in the database

    Returns:
        HttpResponse: A generated http response object to the request to show the lesson set
    """
    print(request)
    return render(request, "data_analysis/setStatistics.html", {'lessonSetData': get_set_stats(setID),
                                                                'lessonSetInfo': get_set_info(setID)})
