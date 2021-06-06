"""
This module contains our Django views for the "data_analysis" application.
"""
from django.shortcuts import render
from data_analysis.py_helper_functions.lesson_stats import get_set_stats, get_set_info
from data_analysis.py_helper_functions.graph_viewer.lesson_reader import lesson_to_json, lesson_info


# Create your views here.
def d3_graph(request, classID, mainSetID, lessonSetIndex):
    """function d3_graph This function handles the view for the graph of a specific lesson

    Args:
        request (HTTPRequest): A http request object created automatically by Django.
        classID (int): ID of the class that user is interested in
        mainSetID (int): ID of the set within the database
        lessonSetIndex (int): index of the lesson set within the main set

    Returns:
        HttpResponse: A generated http response object to the request to generate the graph
    """
    print(request)
    return render(request, "data_analysis/d3graph.html",
                  {'graphData': lesson_to_json(classID, mainSetID, lessonSetIndex, True),
                   'lessonData': lesson_info(mainSetID, lessonSetIndex)})


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
        'mainSetData': get_set_stats(assignmentID), 'mainSetInfo': get_set_info(assignmentID)})
