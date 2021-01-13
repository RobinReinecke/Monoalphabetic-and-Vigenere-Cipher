"""
Module for breaking monoalphabetic cyphers
Uses evolutionary algorithm, to iteratively improve key
"""

from reader import read_ascii_from_file
from mono import Mono
import argparse
import os
import random
import string
import threading
from math import log
from math import inf as INFINITY
# from statistics import mean # Used for iterations amount benchmarking
iteration_amount = 0


ALPHABET = [chr(i) for i in range(97, 97+26)]
MONOGRAM_FILE = os.path.join(os.path.dirname(
    __file__), '../../frequency_files/english_monograms.txt')
N_GRAM_SIZE = 4
N_GRAM_FILE = os.path.join(os.path.dirname(__file__),
                           '../../frequency_files/english_quadgrams_trimmed.txt')
MAX_ITERATIONS = 3000
THREADS = 6


class MonoBreaker:
    """
    Breaks monoalphabetic cyphers
    """

    def __init__(self, monogram_frequencies, n_gram_frequencies):
        """
        Initializes object with given monogram frequency list and n_gram_frequency map
        """
        self.monogram_frequencies = monogram_frequencies
        self.n_grams = n_gram_frequencies
        self.key = ''
        self.score = 0

    @classmethod
    def from_data_files(cls, monogram_file, n_gram_file):
        """
        Initlalize m-gram frequencies
        """
        # Initialize monograms
        monogram_frequencies = {}
        with open(monogram_file, 'r', encoding='utf-8') as freq_file:
            for line in freq_file:
                key, count = line.split(' ')
                if (key != '' and count != ''):
                    monogram_frequencies[key.lower()] = int(count)

        monogram_frequency_list = MonoBreaker._map_to_sorted_list(
            monogram_frequencies)

        # Initialize m-gram frequencies
        # Read from file
        n_grams = {}

        max_val = 0
        with open(n_gram_file, 'r', encoding='utf-8') as file:
            for line in file:
                key, val = line.split(' ')
                n_grams[key.lower()] = int(val)
                max_val = max(max_val, int(val))

        normalize_factor = 1000000 / log(max_val)

        # Calculate logarithm and normalize to integers between 0 and 1 000 000
        for key in n_grams:
            n_grams[key] = int(log(n_grams[key]) * normalize_factor)

        return cls(monogram_frequency_list, n_grams)

    def break_mono_multi(self, text, tries):
        """
        Creates "tries" amount of threads, and runs break_mono individually in
         each of them, then takes the result with the highest overall fitness.
        This basically prevents the possibility returning the wrong key due to
         break_mono being stuck at a local maximum.
        """
        breaker_list = []
        for _ in range(tries):
            new_breaker = self.copy_state()
            thread = threading.Thread(
                target=new_breaker.break_mono, args=(text,))
            thread.start()

            breaker_list.append((thread, new_breaker))

        for thread, _ in breaker_list:
            thread.join()

        return max(breaker_list, key=lambda b: b[1].score)[1].key

    def break_mono(self, text):
        """
        1. Frequency analysis for a key
        2. Score the deciphered text
        3. randomly swap 2 characters in the key and score it again
        4. if score is better, save the new key
        5. repeat
        """
        # global iteration_amount # Used for itertations amounts benchmarking
        parent_key = self.frequency_analysis(text)
        parent_score = -99e9

        deciphered = Mono.decrypt(
            text, parent_key)  # pylint: disable=no-member
        parent_score = self._score(text)

        i = 0
        while i < 3000:
            new_key = list(parent_key)

            # Swap two random characters in the child
            key_swap_a = random.randint(0, 25)
            key_swap_b = random.randint(0, 25)
            new_key[key_swap_a], new_key[key_swap_b] = new_key[key_swap_b], new_key[key_swap_a]

            new_key = ''.join(new_key)
            deciphered = Mono.decrypt(
                text, new_key)  # pylint: disable=no-member
            score = self._score(deciphered)

            # If the child was better, replace the parent with it and restart iterations
            if score > parent_score:
                parent_score = score
                parent_key = new_key
                # iteration_amount += i # Used for itertations amounts benchmarking
                # i = 0 # Reset after a meaningful operation
            else:
                i += 1

        self.key = parent_key
        self.score = parent_score
        return (parent_key, parent_score)

    def _score(self, text):
        """
        Calculate score of the text
        """
        score = 0
        # n_grams = self.n_grams
        for i in range(len(text) - N_GRAM_SIZE + 1):
            n_gram = text[i:i + N_GRAM_SIZE]
            score += self.n_grams[n_gram] if n_gram in self.n_grams else 0

        return score

    def frequency_analysis(self, text):
        """
        Frequency analysis for english texts
        """
        counter = {}
        for letter in string.ascii_lowercase:
            counter[letter] = 0
        for letter in text:
            counter[letter] += 1

        count_list = []
        for letter, count in counter.items():
            count_list.append((count, letter))

        count_list.sort(reverse=True)

        permutation = {}
        for i in range(26):
            permutation[self.monogram_frequencies[i]] = count_list[i][1]

        guessed_key = ''
        for letter in string.ascii_lowercase:
            guessed_key += permutation[letter]
        return guessed_key

    def copy_state(self):
        return self.__class__(list(self.monogram_frequencies), self.n_grams.copy())

    @staticmethod
    def _map_to_sorted_list(frequency_map):
        return sorted(frequency_map, key=frequency_map.__getitem__, reverse=True)


if __name__ == '__main__':
    # Parse arguments
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('file', metavar='FILE',
                        help='The input file.')
    PARSER.add_argument('--out', '-o',
                        help='The output file.')

    ARGS = vars(PARSER.parse_args())

    BREAKER = MonoBreaker.from_data_files(MONOGRAM_FILE, N_GRAM_FILE)
    TEXT = BREAKER.break_mono_multi(
        read_ascii_from_file(ARGS['file']), THREADS)

    if ARGS['out']:
        FILE = open(ARGS['out'], 'w')
        FILE.write(TEXT)
        FILE.close()
    else:
        print(TEXT)

    # BENCHMARK CORRECTNESS
    # tests_correct = 0
    # for test_iteration in range(100):
    #   print(str(test_iteration) + ', ', end='')
    #   # test_key = BREAKER.break_mono(read_ascii_from_file(FILE))
    #   test_key = BREAKER.break_mono_multi(read_ascii_from_file(FILE), THREADS)
    #   if test_key == 'rehmtfzgoxsqwpclbanjdykuiv':
    #     tests_correct += 1
    #     print('SUCCESS: ' + test_key)
    #   else:
    #     print(' FAILED: ' + test_key)

    # print()
    # print(str(tests_correct) + '/100')

    # BENCHMARK AMOUNT OF ITERATIONS NEEDED
    # iteration_amounts = []
    # iteration_amounts_success = []
    # for test_iteration in range(100):
    #   iteration_amount = 0
    #   print(str(test_iteration) + ', ', end='')

    #   test_key = BREAKER.break_mono(read_ascii_from_file(FILE))
    #   if test_key == 'rehmtfzgoxsqwpclbanjdykuiv':
    #     iteration_amounts_success.append(iteration_amount)
    #     print('SUCCESS: ' + str(iteration_amount))
    #   else:
    #     print(' FAILED: ' + str(iteration_amount))
    #   iteration_amounts.append(iteration_amount)

    # print('Maximum Iterations: ' + str(max(iteration_amounts)))
    # print('Average Iterations: ' + str(mean(iteration_amounts)))
    # print('Maximum Iterations (Successfull): ' + str(max(iteration_amounts_success)))
    # print('Average Iterations (Successfull): ' + str(mean(iteration_amounts_success)))
