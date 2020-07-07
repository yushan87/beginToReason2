"""
This module contains model templates for the "core" application. When we create a new item in the database,
a new instance of a model will be made.
"""
from django.db import models


class Code(models.Model):
    """
    Contains a model of the code, allows for the ability to reuse.

    @param models.Model The base model
    """
    code_name = models.CharField(max_length=30)
    lesson_code = models.TextField(max_length=500)

    def __str__(self):
        """
        function __str__ is called to display the name of the code

        Returns:
            str: code name
        """
        return self.code_name


class Reference(models.Model):
    """
    Contains a model of references. Each reference can be used by multiple Lessons.

    @param models.Model The base model
    """
    reference_key = models.CharField(max_length=30)
    reference_text = models.TextField(max_length=250)

    def __str__(self):
        """"
        function __str__ is called to display the reference texts. Helps for admin usability.

        Returns:
            str: reference text
        """
        return self.reference_text


class Question(models.Model):
    """
    Contains a model of Questions. Each question can be used by multiple Lessons.

    @param models.Model The base model
    """
    question_text = models.CharField(max_length=200)

    def __str__(self):
        """"
        function __str__ is called to display the question texts. Helps for admin usability.

        Returns:
            str: question text
        """
        return self.question_text


class McChoice(models.Model):
    """
    Contains a model of Multiple Choice Answers. Each choice is attached to one Question.

    @param models.Model The base model
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    def __str__(self):
        """"
        function __str__ is called to display the multiple choice texts. Helps for admin usability.

        Returns:
            str: choice text
        """
        return self.choice_text


class Reasoning(models.Model):
    """
    Contains a model of Reasoning. There must be a question, and potential to be free response, multiple choice,
    or both. Includes an indicator for type of response needed.

    @param models.Model The base model
    """
    reasoning_name = models.CharField(max_length=30)
    reasoning_question = models.ForeignKey(Question, on_delete=models.CASCADE)

    multiple = 'MC'
    text = 'Text'
    both = 'Both'

    response_options = [
        (multiple, 'Multiple Choice'),
        (text, 'Free Response'),
        (both, "Multiple Choice and Free Response")
    ]

    reasoning_type = models.CharField(
        max_length=4,
        choices=response_options,
        default=multiple
    )

    # Free response has been removed, only because it does not serve a purpose. It belongs in the data collection
    # side of things.

    #free_response_text = models.CharField(max_length=100, default="Enter default message", blank=True)

    mc_set = models.ManyToManyField(McChoice, blank=True)

    def __str__(self):
        """"
        function __str__ is called to display the reasoning key. Due to the potential for multiple reasoning
        activities using the same question, the key must be the identifying feature.

        Returns:
            str: reasoning name
        """
        return self.reasoning_name


class Lesson(models.Model):
    """
    Contains a model of a Lesson.
    Name - For identifying purposes.
    Concept - May be helpful to display to the user.
    Instruction - Directions for how to perform the activity.
    Code - The code activities that student will be interacting with. Will pull from the Code model.
    Reference Set - May contain multiple references, or no references at all.
    Reason - There is only one reasoning activity allowed per Lesson. May contain mc, fr, or both.
    Screen_Record - Boolean for whether or not to record the activity.

    @param models.Model The base model
    """
    lesson_name = models.CharField(max_length=50)
    lesson_concept = models.CharField(max_length=50)
    instruction = models.TextField()
    code = models.ForeignKey(Code, on_delete=models.CASCADE)
    reference_set = models.ManyToManyField(Reference, blank=True)
    reason = models.ForeignKey(Reasoning, on_delete=models.CASCADE, blank=True)
    screen_record = models.BooleanField()

    def __str__(self):
        """"
        function __str__ is called to display the Lesson name. This will be useful for admin/educators when
        building the Lesson Plan
        Returns:
            str: lesson name
        """
        return self.lesson_name
