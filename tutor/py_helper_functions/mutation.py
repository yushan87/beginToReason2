"""
This module contains our Django helper functions for the "mutate" application.
"""
import random

letters = [['X', 'Y', 'Z'], ['L', 'M', 'N'], ['I', 'J', 'K'], ['E', 'F', 'G']]
variable_key = {}
inverse_variable_key = {}


def mutate(activity_string):
    """function mutate This function changes a random mixture of the letters, numbers, and symbols in the exercise
    Args:
         activity_string (string): string of activity to be mutated
         letters (2D array): array of groups of letters to use in exercise
         variable_key (dict): maps the original variables with the new ones
         inverse_variable_key (dict): maps the new variables to the old ones
    Returns:
        String: A string of the mutated activity
    """
    mutate_vars(activity_string)
    mutate_numbers(activity_string)

    # reset index and iterate through string
    index = 0
    while index < len(activity_string) - 1:
        character = activity_string[index]

        for var in variable_key:
            if character == var:
                # only if it is followed by certain things so we do not change Integer and If etc
                if not activity_string[index + 1].isalpha():
                    activity_string = activity_string[:index] + str(variable_key[var]) + activity_string[index + 1:]
        index = index + 1

    return activity_string


def mutate_vars(activity_string):
    """function mutate_vars This function stores the original variables in variable_key and inverse_variable_key
         with variables from the letters array to be later substituted in mutate
    Args:
         activity_string (string): string of activity to be mutated
         letters (2D array): array of groups of letters to use in exercise
         variable_key (dict): maps the original variables with the new ones
         inverse_variable_key (dict): maps the new variables to the old ones
    Returns:
        NULL
    """
    # find where it says Var in string and store index
    index = activity_string.index("Var ")

    # index is at V so add 4
    index = index + 4
    letter = activity_string[index]
    variable_list = []
    # while the current index in the string does not point to : (to get the variable out)
    while letter != ':':
        if letter != ' ' and letter != ',':
            variable_list.append(letter)
        index = index + 1
        letter = activity_string[index]

    # need to pick a random number between 0 and len of letters inclusive
    random_num = int(random.uniform(0, len(letters)))
    i = 0

    #maybe shuffle lists? maybe not
    if random.randint(0, 1) == 1:
        random.shuffle(letters[random_num])
    # list is now a list of the variables to find and switch
    # iterate through the list and assign each variable a new letter
    for var in variable_list:

        # assign each variable a new variable in the randomNum sub array
        variable_key[var] = letters[random_num][i]
        # make an inverse map
        inverse_variable_key[letters[random_num][i]] = var
        i = i + 1


def mutate_numbers(activity_string):
    """function mutate_numbers This function stores the original variables in variable_key and inverse_variable_key
        with either incremented or decremented values
    Args:
         activity_string (string): string of activity to be mutated
         variable_key (dict): maps the original variables with the new ones
         inverse_variable_key (dict): maps the new variables to the old ones
    Returns:
        NULL
    """
    index = 0
    increment_value = 1
    variable_list = []

    rand_num = random.randint(1, 2)
    if rand_num == 1:
        while index < len(activity_string) - 1:
            character = activity_string[index]
            # if character is a digit that we have not found before... put it in variable list
            if character.isdigit() and character not in variable_list:
                variable_list.append(character)
            index = index + 1

        for digit in variable_list:
            if int(digit) == 3:
                increment_value = -1

        for digit in variable_list:
            variable_key[digit] = str(int(digit) + increment_value)
            inverse_variable_key[str(int(digit) + increment_value)] = digit


def mutate_symbols():
    """function mutate_symbols This function stores various symbols and their opposite symbol in the variable and inverse
        variable keys, not currently used in mutate
    Args:
         variable_key (dict): maps the original variables with the new ones
         inverse_variable_key (dict): maps the new variables to the old ones
    Returns:
        NULL
    """
    variable_key['>'] = '<'
    variable_key['<'] = '>'
    variable_key['>='] = '<='
    variable_key['<='] = '>='
    inverse_variable_key['>'] = '<'
    inverse_variable_key['<'] = '>'
    inverse_variable_key['>='] = '<='
    inverse_variable_key['<='] = '>='


def reverse_mutate(activity_string):
    """function mutate_symbols This function uses the variables stored in inverse_variable_key to reverse the string to
            its original form
    Args:
        activity_string (string): string of activity to be mutated
        inverse_variable_key (dict): maps the new variables to the old ones
    Returns:
        NULL
        """
    index = 0
    while index < len(activity_string) - 1:
        character = activity_string[index]
        for var in inverse_variable_key:
            if character == var:
                # only if it is followed by certain things so we do not change Integer and If etc
                if not activity_string[index + 1].isalpha():
                    activity_string = activity_string[:index] + str(inverse_variable_key[var]) + activity_string[index + 1:]
        index = index + 1
    return activity_string


def can_mutate(current_lesson):
    """function can_mutate this function checks if you can mutate and returns the code
        Args:
            current lesson to get the user information
        Returns:
            mutated_code the code string whether it has been mutated or not
    """
    # check if can mutate
    mutated_code = current_lesson.code.lesson_code
    if current_lesson.can_mutate:
        mutated_code = mutate(current_lesson.code.lesson_code)
    return mutated_code


def get_inv_key():
    """function get_inv_key returns the inv key
        Args:
            NULL
        Returns:
            inverse_variable_key the key string
    """
    return inverse_variable_key

