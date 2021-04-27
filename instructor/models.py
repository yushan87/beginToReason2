"""
This module contains model templates for the "instructor" application. When we create a new item in the database,
a new instance of a model will be made.
"""
from datetime import date

from django.core.validators import MinLengthValidator
from django.db import models

from accounts.models import UserInformation
from core.models import MainSet


class Class(models.Model):
    """
    A model of a class

    @param models.Model The base model
    """
    class_name = models.CharField("Name", max_length=100, validators=[MinLengthValidator(1)])  # Class name field
    join_code = models.CharField("Join_Code", max_length=6, validators=[MinLengthValidator(6)], unique=True)  # Code for joining class

    def __str__(self):
        """function __str__ is used to create a string representation of this class

        Returns:
            str: user email
        """
        return self.class_name

    def user_count(self):
        """function user_count is used to count how many students are in a class

        Returns:
            int: count of how many non-instructor users are enrolled
        """
        return ClassMembership.objects.filter(class_taking_id=self.id, is_instructor=False).count()

    def get_assignments(self):
        """function get_classes_taught This function gives assignments of a class

        Returns:
            List: List of assignments from a class
        """
        return Assignment.objects.filter(class_key_id=self.id).all()

    def get_current_assignments(self):
        """function get_classes_taught This function gives assignments of a class that are currently assigned

        Returns:
            List: List of assignments from a class
        """
        today = date.today()
        return Assignment.objects.filter(class_key_id=self.id, start_date__lte=today, end_date__gte=today).all()

    def get_future_assignments(self):
        """function get_classes_taught This function gives assignments of a class that haven't opened yet

        Returns:
            List: List of assignments from a class
        """
        return Assignment.objects.filter(class_key_id=self.id, start_date__gt=date.today()).all()

    def get_past_assignments(self):
        """function get_classes_taught This function gives assignments of a class that have closed already

        Returns:
            List: List of assignments from a class
        """
        return Assignment.objects.filter(class_key_id=self.id, end_date__lt=date.today()).all()

    def next_lesson_due_date(self):
        """function next_lesson_due_date handles finding the nearest due date of all lessons for a class

        Returns:
            Date: Date of nearest due assignment
        """
        record = date.max
        for assignment in self.get_current_assignments():
            if assignment.end_date < record:
                record = assignment.end_date

        if record == date.max:
            return None
        return record

    def get_students(self):
        """function get_students handles finding all non-instructor students in a class

        Returns:
            List: List of non-instructor students
        """
        membership_list = ClassMembership.objects.filter(class_taking=self, is_instructor=False)

        students_list = []
        for membership in membership_list:
            students_list.append(membership.user)

        return sorted(students_list, key=lambda x: x.user.last_login, reverse=True)

    def get_instructors(self):
        """function get_instructors handles finding all instructors of a class

        Returns:
            List: List of instructors
        """
        membership_list = ClassMembership.objects.filter(class_taking=self, is_instructor=True)

        instructors_list = []
        for membership in membership_list:
            instructors_list.append(membership.user)

        return sorted(instructors_list, key=lambda x: x.user.last_login, reverse=True)


class Assignment(models.Model):
    """
    A class-specific main set with a start and end date

    @param models.Model The base model
    """
    class_key = models.ForeignKey(Class, on_delete=models.CASCADE)  # Class this was assigned to
    main_set = models.ForeignKey(MainSet, on_delete=models.CASCADE)  # Main set assigned
    start_date = models.DateField(default=date.today)
    end_date = models.DateField()

    def start_date_iso(self):
        """function start_date_iso formats start date for ISO for HTML

        Returns:
            String: Start date in YYYY-MM-DD ISO format
        """

        return self.start_date.isoformat()

    def end_date_iso(self):
        """function end_date_iso formats due date for ISO for HTML

        Returns:
            String: Due date in YYYY-MM-DD ISO format
        """

        return self.end_date.isoformat()


class ClassMembership(models.Model):
    """
    A many-to-many containing a boolean signifying whether user is instructor of class or not

    @param models.Model The base model
    """
    user = models.ForeignKey(UserInformation, on_delete=models.CASCADE)
    class_taking = models.ForeignKey(Class, on_delete=models.CASCADE)
    is_instructor = models.BooleanField(default=False)
