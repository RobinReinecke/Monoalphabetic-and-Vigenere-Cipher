"""
Module for reading file contents
"""

import string


def read_ascii_from_file(file):
    """
    Used to read alphabetic characters from file and turn them to lowercase
    """
    FILE = open(file, 'r')  # pylint: disable=invalid-name
    text = FILE.read()
    result = ''
    for letter in text.lower():
        if letter in string.ascii_lowercase:
            result += letter
    FILE.close()
    return result
