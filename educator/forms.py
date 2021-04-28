"""
This module contains custom forms used to collect the information needed to create a model.
"""
from django import forms
from accounts.models import UserInformation, Class


class ClassForm(forms.ModelForm):
    """
    This form creates an instance of a Class model and collects its fields
    """

    class_name = forms.CharField(label='Class Name', max_length=100)  # Class name field
    school = forms.CharField(label='School Name', max_length=100)  # Class name field
    class_instructor = forms.ModelMultipleChoiceField(label='Additional Instructors', queryset=UserInformation.objects.all())

    def __init__(self, *args, **kwargs):
        """function __init__ is called to instantiate the user information form

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)

        # Validator that makes sure all the fields have been filled in
        for _field_name, field in self.fields.items():
            field.required = True
            if _field_name == "class_instructor":
                field.required = False

    class Meta:
        """
        A class that stores the meta information about this form
        """
        model = Class
        fields = ['class_name', 'school', 'class_instructor']
