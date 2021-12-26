"""
This module contains our Django views for the "data_analysis" application.
"""
from accounts.models import UserInformation
from data_analysis.py_helper_functions.graph_viewer.lesson_reader import lesson_to_json, lesson_info
from data_analysis.py_helper_functions.lesson_stats import get_main_set_stats, get_main_set_info
from django.shortcuts import render, redirect
from educator.models import Assignment
from educator.py_helper_functions.educator_helper import user_educates_class_auth


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
    # Value checking
    try:
        assignment = Assignment.objects.get(id=assignmentID)
        current_user = UserInformation.objects.get(user=request.user)
        if user_educates_class_auth(current_user, assignment.class_key.id):
            lesson_set = assignment.main_set.set_by_index(lessonSetIndex)
            if lesson_set is not None:
                if lesson_set.lesson_by_index(lessonIndex) is not None:
                    return render(request, "data_analysis/d3graph.html",
                                  {'graphData': lesson_to_json(assignmentID, lessonSetIndex, lessonIndex, True),
                                   'lessonData': lesson_info(assignmentID, lessonSetIndex, lessonIndex)})
    except Assignment.DoesNotExist:
        pass

    return redirect("accounts:profile")


def assignment_statistics(request, assignmentID):
    """function d3_graph This function handles the view for lesson set-wide stats

    Args:
        request (HTTPRequest): A http request object created automatically by Django.
        assignmentID (int): ID of the assignment that user is interested in

    Returns:
        HttpResponse: A generated http response object to the request to show the lesson set
    """
    # Value checking
    try:
        assignment = Assignment.objects.get(id=assignmentID)
        current_user = UserInformation.objects.get(user=request.user)
        if user_educates_class_auth(current_user, assignment.class_key.id):
            return render(request, "data_analysis/mainSetStatistics.html", {
                'mainSetData': get_main_set_stats(assignmentID), 'mainSetInfo': get_main_set_info(assignmentID)})
    except Assignment.DoesNotExist:
        pass

    return redirect("accounts:profile")
