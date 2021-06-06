"""
This module contains our Django views for the "data_analysis" application.
"""
from django.shortcuts import render
from data_analysis.py_helper_functions.lesson_stats import get_main_set_stats, get_main_set_info
from data_analysis.py_helper_functions.graph_viewer.lesson_reader import lesson_to_json, lesson_info


# Create your views here.
def d3_graph(request, assignmentID, lessonSetIndex, lessonIndex):
    """function d3_graph This function handles the view for the graph of a specific lesson

    Args:
        request (HTTPRequest): A http request object created automatically by Django.
        assignmentID (int): ID of the assignment that user is interested in
        lessonSetIndex (int): index of the lesson set within the main set
        lessonIndex (int): index of the desired lesson within the lesson set

    Returns:
        HttpResponse: A generated http response object to the request to generate the graph
    """
    print(request)
    return render(request, "data_analysis/d3graph.html",
                  {'graphData': lesson_to_json(assignmentID, lessonSetIndex, True),
                   'lessonData': lesson_info(assignmentID, lessonSetIndex)})


def assignment_statistics(request, assignmentID):
    """function d3_graph This function handles the view for lesson set-wide stats

    Args:
        request (HTTPRequest): A http request object created automatically by Django.
        assignmentID (int): ID of the assignment that user is interested in

    Returns:
        HttpResponse: A generated http response object to the request to show the lesson set
    """
    print(request)
    return render(request, "data_analysis/mainSetStatistics.html", {
        'mainSetData': get_main_set_stats(assignmentID), 'mainSetInfo': get_main_set_info(assignmentID)})
