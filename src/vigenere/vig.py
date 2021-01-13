"""
Vigenere encryption and decryption module
"""

import argparse
import string
from reader import read_ascii_from_file


class Vigenere:
    """
    Class implementing encryption and decryption of vigenere cyphers
    """

    @staticmethod
    def text_to_numbers(text):
        """
        Creates an array with number of shifts extracted from passed text
        """
        shifts = []
        for letter in text:
            shifts.append(string.ascii_lowercase.index(letter.lower()))
        return shifts

    @staticmethod
    def encrypt(text, key):
        """
        Encrypts the vigenere cypher
        """
        # create an array with number of shifts extracted from passed key
        key_shifts = Vigenere.text_to_numbers(key)

        result = ''
        key_pos = 0
        for letter in text.lower():
            if letter in string.ascii_lowercase:
                # shift letter
                index = string.ascii_lowercase.index(letter)
                index = (index + key_shifts[key_pos]) % 26
                result += string.ascii_lowercase[index]

                # move key_pos
                key_pos = (key_pos + 1) % len(key)
            else:
                result += letter
        return result

    @staticmethod
    def decrypt(text, key):
        """
        Decrypts the cigenere cypher
        """
        key_shifts = Vigenere.text_to_numbers(key)
        decrypt_key = [string.ascii_letters[26 - shift]
                       for shift in key_shifts]
        return Vigenere.encrypt(text, decrypt_key)


PARSER = argparse.ArgumentParser()
CRYPT = PARSER.add_mutually_exclusive_group(required=True)

CRYPT.add_argument('--encrypt', '-e', metavar='KEY',
                   help='specify encryption key.')
CRYPT.add_argument('--decrypt', '-d', metavar='KEY',
                   help='specify decryption key.')

PARSER.add_argument('file', metavar='FILE',
                    help='the input file.')
PARSER.add_argument('--out', '-o',
                    help='The output file.')

ARGS = vars(PARSER.parse_args())

TEXT = ''
if ARGS['encrypt']:
    TEXT = Vigenere.encrypt(read_ascii_from_file(
        ARGS['file']), ARGS['encrypt'])
elif ARGS['decrypt']:
    TEXT = Vigenere.decrypt(read_ascii_from_file(
        ARGS['file']), ARGS['decrypt'])

if ARGS['out']:
    FILE = open(ARGS['out'], 'w')
    FILE.write(TEXT)
    FILE.close()
else:
    print(TEXT)
