"""
This module contains our Django views for the "data_analysis" application.
"""
from django.shortcuts import render, redirect
from tutor.py_helper_functions.tutor_helper import user_auth_inst, lesson_set_auth
from data_analysis.py_helper_functions.lesson_stats import get_set_stats, get_set_info
from data_analysis.py_helper_functions.graph_viewer.lesson_reader import lesson_to_json, lesson_info


# Create your views here.
def d3_graph(request, setID, lessonIndex):
    """function d3_graph This function handles the view for the graph of a specific lesson

    Args:
        request (HTTPRequest): A http request object created automatically by Django.

    Returns:
        HttpResponse: A generated http response object to the request to generate the graph
    """
    print(request)
    return render(request, "data_analysis/d3graph.html", {'graphData': lesson_to_json(setID, lessonIndex, True),
                                                          'lessonData': lesson_info(setID, lessonIndex)})


def set_statistics(request, index):
    """function d3_graph This function handles the view for lesson set-wide stats

    Args:
        request (HTTPRequest): A http request object created automatically by Django.

    Returns:
        HttpResponse: A generated http response object to the request to show the lesson set
    """
    print(request)
    return render(request, "data_analysis/setStatistics.html", {'lessonSetData': get_set_stats(index),
                                                                'lessonSetInfo': get_set_info(index)})


def instructor(request):
    """function instructor This function handles the view for the instructor page of the application.

    Args:
        request (HTTPRequest): A http request object created automatically by Django.

    Returns:
        HttpResponse: A generated http response object to the request.
    """

    # get all lesson sets, display
    if request.method == 'POST':
        # Will this include where the data is updated? Such as selecting different visuals to interact with?
        if user_auth_inst(request):
            # Take instructor to data view
            if lesson_set_auth(request):
                return redirect("/tutor/tutor")
            else:
                return redirect("accounts:profile")
        else:
            return redirect("/accounts/settings")
    else:
        return render(request, "data_analysis/visual.html")
