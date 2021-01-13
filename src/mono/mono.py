"""
Monoalphabetic encryption and decryption module
"""

import argparse
import string
from reader import read_ascii_from_file


class Mono:
    """
    Class implementing encryption and decryption of monoalphabetic cyphers
    """
    @staticmethod
    def encrypt(text, key):
        """
        Encrypts the monoalphalbetic cypher
        """
        # create a dictonary for the passed key-alphabet
        dictionary = {}
        for letter, key_letter in zip(string.ascii_lowercase, key):
            dictionary[letter] = key_letter

        result = ''
        for letter in text.lower():
            if letter in string.ascii_lowercase:
                result += dictionary[letter]
            else:
                result += letter
        return result

    @staticmethod
    def decrypt(text, key):
        """
        Decrypts the monoalphalbetic cypher
        """
        # create reversed dictionary
        dictionary = {}
        for key_letter, letter in zip(key, string.ascii_lowercase):
            dictionary[key_letter] = letter

        result = ''
        for letter in text.lower():
            if letter in string.ascii_lowercase:
                result += dictionary[letter]
            else:
                result += letter
        return result


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser()
    CRYPT = PARSER.add_mutually_exclusive_group(required=True)

    CRYPT.add_argument('--encrypt', '-e', metavar='KEY',
                       help='Specify encryption key.')
    CRYPT.add_argument('--decrypt', '-d', metavar='KEY',
                       help='Specify decryption key.')

    PARSER.add_argument('file', metavar='FILE',
                        help='The input file.')
    PARSER.add_argument('--out', '-o',
                        help='The output file.')

    ARGS = vars(PARSER.parse_args())

    TEXT = ''
    if ARGS['encrypt']:
        TEXT = Mono.encrypt(read_ascii_from_file(
            ARGS['file']), ARGS['encrypt'].lower())
    elif ARGS['decrypt']:
        TEXT = Mono.decrypt(read_ascii_from_file(
            ARGS['file']), ARGS['decrypt'].lower())

    if ARGS['out']:
        FILE = open(ARGS['out'], 'w')
        FILE.write(TEXT)
        FILE.close()
    else:
        print(TEXT)
