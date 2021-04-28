"""
This module contains our Django helper functions for the "instructor" application.
"""
from instructor.models import ClassMembership, Class, Assignment


def user_is_instructor(user_info):
    """function user_is_instructor This function handles the auth logic for an instructor

    Args:
        user_info: Model from accounts

    Returns:
        Boolean: A boolean to signal if the user instructs any class
    """
    return user_info.user_instructor


def user_auth_inst(user_info, class_id):
    """function user_auth_inst This function handles the auth logic for an instructor of a class

    Args:
        user_info: Model from accounts
        class_id (int): ID of the class in question

    Returns:
        Boolean: A boolean to signal if the user instructs class in question
    """
    membership = user_in_class_auth(user_info, class_id)
    if membership is not None:
        return membership.is_instructor
    return False


def user_in_class_auth(user_info, class_id):
    """function user_in_class_auth This function handles the auth logic for users in classes

    Args:
        user_info: Model from accounts
        class_id (int): ID of the class in question

    Returns:
        ClassMembership: The relationship between the two, or None if doesn't exist
    """
    try:
        return ClassMembership.objects.get(user_id=user_info.id, class_taking=class_id)
    except ClassMembership.DoesNotExist:
        return None


def get_classes(user_info):
    """function get_classes This function gives classes a user is in

    Args:
        user_info: Model from accounts

    Returns:
        classes: List of classes the user is in
    """
    class_ids = []
    for membership in ClassMembership.objects.filter(user_id=user_info.id):
        class_ids.append(membership.class_taking_id)

    classes = []
    for class_id in class_ids:
        classes.append(Class.objects.get(id=class_id))

    return classes


def get_classes_taught(user_info):
    """function get_classes_taught This function gives classes a user teaches

    Args:
        user_info: Model from accounts

    Returns:
        classes: List of classes the user teaches
    """
    class_ids = []
    for membership in ClassMembership.objects.filter(user_id=user_info.id, is_instructor=1):
        class_ids.append(membership.class_taking_id)

    classes = []
    for class_id in class_ids:
        classes.append(Class.objects.get(id=class_id))

    return classes
