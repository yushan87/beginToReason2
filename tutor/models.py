"""
This module contains model templates for the "tutor" application. When we create a new item in the database,
a new instance of a model will be made.
"""
from django.db import models

# Create your models here.





class Lesson(models.Model):
    """
    TODO: Need to fill in the correct information for this class after
          remove experimental things that don't work.
    """
    lesson_name = models.CharField(max_length=30)
    lesson_concept = models.CharField(max_length=50)
    lesson_code = models.TextField(max_length=500)

    def __str__(self):
        """function __str__ TODO: Need to fill in the correct information for this function.

        Returns:
            str: TODO: Need to fill in the correct information for this function.
        """
        return self.lesson_name



class Instruction(models.Model):
    instruction_key = models.CharField(max_length=30)
    instruction_text = models.TextField(max_length=250)

    # lesson = models.ManyToManyField(Lesson, related_name='references')#, through= 'LessonReferences')

    def __str__(self):
        return self.reference_key



class Reference(models.Model):
    """
    TODO: Need to fill in the correct information for this class after
          remove experimental things that don't work.
    """
    reference_key = models.CharField(max_length=30)
    reference_text = models.TextField(max_length=250)

    # lesson = models.ManyToManyField(Lesson, related_name='references')#, through= 'LessonReferences')

    def __str__(self):
        """function __str__ TODO: Need to fill in the correct information for this function.

        Returns:
            str: TODO: Need to fill in the correct information for this function.
        """
        return self.reference_key




class Question(models.Model):
    question_text = models.CharField(max_length=200)

    def __str__(self):
        return self.question_text

class MC_Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    
    def __str__(self):
        return self.choice_text

class MC_Set(models.Model):
    set_name = models.CharField(max_length=200)
    def __str__(self):
        return self.set_name


class Free_Resp(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    response_text = models.CharField(max_length=100,default="Enter default message")
    def __str__(self):
        return self.response_text

class Reasoning(models.Model):

    reasoning_key = models.CharField(max_length=30)
    reasoning_text = models.ForeignKey(Question, on_delete=models.CASCADE)
    # lesson = models.ManyToManyField(Lesson, related_name='references')#, through= 'LessonReferences')

    MULTIPLE = 'MC'
    TEXT = 'Text'

    RESPONSE_OPTIONS = [
        (MULTIPLE, 'Multiple Choice'),
        (TEXT, 'Text Response'),
    ]

    reasoning_type = models.CharField(
        max_length=4,
        choices=RESPONSE_OPTIONS,
        default=MULTIPLE
    )

    #if mc, self.mc_choice_set.all() returns all the choices
    #associated with this question


    def __str__(self):
        return self.reasoning_key








class CodeTemplate(models.Model):
    """
    TODO: Need to fill in the correct information for this class after
          remove experimental things that don't work.
    """
    template_name = models.CharField(max_length=30)
    template_code = models.TextField(max_length=500)

    def __str__(self):
        """function __str__ TODO: Need to fill in the correct information for this function.

        Returns:
            str: TODO: Need to fill in the correct information for this function.
        """
        return self.template_name
