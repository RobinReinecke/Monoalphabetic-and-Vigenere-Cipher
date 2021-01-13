"""
Module for breaking vigenere cyphers
"""

import argparse
import os
from math import log
from reader import read_ascii_from_file


MONOGRAM_FILE = os.path.join(os.path.dirname(
    __file__), '../../frequency_files/english_monograms.txt')
BIGRAM_FILE = os.path.join(os.path.dirname(
    __file__), '../../frequency_files/english_bigrams.txt')


class VigenereBreaker:  # pylint: disable=too-few-public-methods
    """
    Vigenere Cipher Breaker class
    """

    def __init__(self, key_length, monogram_file, bigram_file):
        self.key_length = key_length

        # Initialize monograms
        monogram_frequencies = {}
        with open(monogram_file, 'r', encoding='utf-8') as freq_file:
            for line in freq_file:
                key, count = line.split(' ')
                monogram_frequencies[key.lower()] = int(count)

        self.monogram_frequencies = VigenereBreaker._map_to_sorted_list(
            monogram_frequencies)

        # Initialize bigrams
        self.bigram_map = VigenereBreaker._import_bigram_file(bigram_file)

    def break_vigenere(self, text):
        """
        Attempts to break vignere cipher using bigram analysis
        Tries out all different key bigrams, rating them based on the resulting
          distribution of decyphered bigrams, then picks the best combination of
          those keys
        """

        key_guesses = [['' for i in range(self.key_length)], [
            '' for i in range(self.key_length)]]
        key_fitness = [0 for i in range(self.key_length)]

        # Split into as many groups as there are letters in the key
        text_fragments = VigenereBreaker._split_text(self.key_length, text)

        # Iterate through all positions in the key
        for i in range(self.key_length):
            # Concatenate adjacent text fragments into bigram lists
            bigram_list = [text_fragments[i][c] +
                           text_fragments[(i+1) % self.key_length][c +
                                                                   int((i+1) / self.key_length)]
                           for c in range(min(len(text_fragments[i]),
                                              len(text_fragments[(i+1) % self.key_length]) -
                                              int((i+1) / self.key_length)))]

            # Iterate through all possible key snippets for the current bigrams
            best_key = 'aa'
            best_fitness = 0
            for j in range(26*26):
                key = chr(int(j / 26) + 97) + chr(int(j % 26) + 97)
                translated_bigram_list = self._tanslate_bigram_list(
                    bigram_list, key)
                translated_fitness = self._get_fitness(translated_bigram_list)
                if translated_fitness > best_fitness:
                    best_fitness = translated_fitness
                    best_key = key

            # Insert into appropiate positions in both key guesses to be compared later
            key_guesses[0][i] = best_key[0]
            key_guesses[1][(i + 1) % self.key_length] = best_key[1]
            key_fitness[i] = best_fitness

        # Generate final key
        key = ''
        for i in range(self.key_length):
            key += (key_guesses[0][i] if key_fitness[i] > key_fitness[(i-1) % self.key_length]
                    else key_guesses[1][i])

        # Invert key into correct form
        return self._invert_key(key)

    def _get_fitness(self, bigram_list):
        """
        Calculate fitness of given bigram list based on the logarithmic frequency table
        """
        fitness = 0
        for bigram in bigram_list:
            fitness += self.bigram_map[ord(bigram[0]) -
                                       97][ord(bigram[1]) - 97]

        return fitness

    @staticmethod
    def _invert_key(key):
        """
        Inverts the given key a <-> a, b <-> z, etc.
        """
        inverted_key = ''
        for char in key:
            inverted_key += chr((26 - (ord(char) - 97)) % 26 + 97)

        return inverted_key

    @staticmethod
    def _tanslate_bigram_list(bigram_list, key):
        """
        Decypher the given bigram list with the given key
        IMPORTANT: Uses inverted key compared to the ones used in vig.py
        """
        new_bigrams = []
        shift_a = ord(key[0]) - 97
        shift_b = ord(key[1]) - 97

        for bigram in bigram_list:
            new_bigrams.append(chr((ord(bigram[0]) - 97 + shift_a) % 26 + 97) +
                               chr((ord(bigram[1]) - 97 + shift_b) % 26 + 97))

        return new_bigrams

    @staticmethod
    def _import_bigram_file(file_name):
        """
        Imports bigrams from file into 2D array using ASCII - 97 indices
        """
        bigram_map = [[1 for i in range(26)] for j in range(26)]

        with open(file_name, 'r', encoding='utf-8') as file:
            for line in file:
                key, val = line.split(' ')
                key = key.lower()
                bigram_map[ord(key[0]) - 97][ord(key[1]) - 97] = int(val)

        # Calculate logarithm
        max_log = 0
        for row, _ in enumerate(bigram_map):
            for col, _ in enumerate(bigram_map[row]):
                bigram_map[row][col] = log(bigram_map[row][col])
                max_log = max(max_log, bigram_map[row][col])

        normalize_factor = 1000000 / max_log

        # Normalize to integers between 0 and 1 000 000
        for row, _ in enumerate(bigram_map):
            for col, _ in enumerate(bigram_map[row]):
                bigram_map[row][col] = int(
                    bigram_map[row][col] * normalize_factor)
                max_log = max(max_log, bigram_map[row][col])

        return bigram_map

    @staticmethod
    def _split_text(key_len, text):
        """
        Splits the text into key_len groups, such that all letters affected by a
        position in the key are in one group
        """
        split_text = ['' for i in range(key_len)]
        for c, char in enumerate(text):
            split_text[c % key_len] += char
        return split_text

    @staticmethod
    def _map_to_sorted_list(frequency_map):
        """
        Returns the elements of a given frequency map, sorted in descending order
        """
        return sorted(frequency_map, key=frequency_map.__getitem__, reverse=True)


if __name__ == '__main__':
    # Parse arguments
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('file', metavar='FILE',
                        help='The input file.')
    PARSER.add_argument('--keylen', '-k', required=True,
                        help='The length of the key used.')
    PARSER.add_argument('--out', '-o',
                        help='The output file.')

    ARGS = vars(PARSER.parse_args())

    BREAKER = VigenereBreaker(int(ARGS['keylen']), MONOGRAM_FILE, BIGRAM_FILE)
    TEXT = BREAKER.break_vigenere(read_ascii_from_file(ARGS['file']))

    if ARGS['out']:
        FILE = open(ARGS['out'], 'w')
        FILE.write(TEXT)
        FILE.close()
    else:
        print(TEXT)
