"""
This module contains our Django helper functions for the "mutate" application.
"""
import random


def mutate(activity_string, letters, variable_key, inverse_variable_key):
    """function mutate This function changes a random mixture of the letters, numbers, and symbols in the exercise
    Args:
         activity_string (string): string of activity to be mutated
         letters (2D array): array of groups of letters to use in exercise
         variable_key (dict): maps the original variables with the new ones
         inverse_variable_key (dict): maps the new variables to the old ones
    Returns:
        String: A string of the mutated activity
    """
    # generate a random number to decide how many times to loop through and mutate things
    random_num = random.randint(0, 2)
    index = 0

    while index < random_num:
        # which_mutate decides which category to mutate each iteration of loop
        which_mutate = random.randint(0, 2)
        if which_mutate == 0:
            mutate_vars(activity_string, letters, variable_key, inverse_variable_key)
        elif which_mutate == 1:
            mutate_numbers(activity_string, variable_key, inverse_variable_key)
        elif which_mutate == 2:
            mutate_symbols(variable_key, inverse_variable_key)
        index = index + 1

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


def mutate_vars(activity_string, letters, variable_key, inverse_variable_key):
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

    # need to pick a random number between 0 and 3 inclusive
    random_num = int(random.uniform(0, len(letters)))
    i = 0

    # list is now a list of the variables to find and switch
    # iterate through the list and assign each variable a new letter
    for var in variable_list:
        # assign each variable a new variable in the randomNum sub array
        variable_key[var] = letters[random_num][i]
        # make an inverse map
        inverse_variable_key[letters[random_num][i]] = var
        i = i + 1


def mutate_numbers(activity_string, variable_key, inverse_variable_key):
    """function mutate_numbers This function stores the original variables in variable_key and inverse_variable_key
        with different random numbers 0-3
    Args:
         activity_string (string): string of activity to be mutated
         variable_key (dict): maps the original variables with the new ones
         inverse_variable_key (dict): maps the new variables to the old ones
    Returns:
        NULL
    """
    index = 0
    while index < len(activity_string) - 1:
        character = activity_string[index]
        # if you character is a digit that we have not found before... put it in map and reverse map
        if character.isdigit() and character not in variable_key:
            random_num = random.randint(0, 3)
            while random_num in inverse_variable_key or random_num == character:
                random_num = random.randint(0, 3)
            variable_key[character] = random_num
            inverse_variable_key[random_num] = [character]
        index = index + 1


def mutate_symbols(variable_key, inverse_variable_key):
    """function mutate_symbols This function stores various symbols and their opposite symbol in the variable and inverse
        variable keys
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


def reverse_mutate(activity_string, inverse_variable_key):
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
