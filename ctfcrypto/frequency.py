import os
import json

from .util import *

letter_frequency = []
tetragram_frequency = []

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


def load_frequencies():
    global letter_frequency
    global tetragram_frequency
    global __location__

    json_file = open(os.path.join(__location__ , os.path.join('data', 'frequencies.json')), 'r')
    json_contents = json.load(json_file)
    letter_frequency = json_contents['letter_frequency']
    tetragram_frequency = json_contents['tetragram_frequency']

# Generating letter and tetragram frequencies:
def generate_frequencies():
    global letter_frequency
    global tetragram_frequency
    global __location__

    book_file_names = ['plato-republic', 'hawthorne-scarlet-letter', 'dickens-tale-of-two-cities',
                       'douglass-narrative-of-the-life-of-frederick-douglass']

    letter_frequency = [0] * 26
    tetragram_frequency = [0] * (26 ** 4)

    total_characters = 0
    total_tetragrams = 0

    for book_file_name in book_file_names:
        book = open(os.path.join(__location__ , os.path.join('data', book_file_name + '.txt')), 'r')
        text = book.read()
        clean_text = ''.join(str(character if character in string.ascii_lowercase else '')
                             for character in text.lower())
        for character in clean_text:
            letter_frequency[ord(character) - ord('a')] += 1
            total_characters += 1
        for i in range(len(clean_text) - 3):
            word = clean_text[i:i + 4]
            tetragram = sum((ord(word[j]) - ord('a')) * (26 ** (3 - j)) for j in range(4))
            tetragram_frequency[tetragram] += 1
            total_tetragrams += 1
    for i in range(26):
        letter_frequency[i] /= total_characters
    for i in range(26 ** 4):
        tetragram_frequency[i] /= total_tetragrams
    json_object = {'tetragram_frequency': tetragram_frequency, 'letter_frequency': letter_frequency}
    json_file = open(os.path.join(__location__ , os.path.join('data', 'frequencies.json')), 'w')
    json.dump(json_object, json_file)


def letter_frequency_cost(sequence):
    clean_sequence = clean_text(sequence)
    total_letters = len(clean_sequence)
    frequency = [(clean_sequence.lower().count(chr(ord('a') + i))) / total_letters for i in range(26)]
    cost = sum(abs(frequency[i] - letter_frequency[i]) for i in range(26))
    return cost / 2


def letter_to_index(character):
    if character in string.ascii_lowercase:
        return ord(character) - ord('a')
    elif character in string.ascii_uppercase:
        return ord(character) - ord('A')
    return None


def index_of_coincidence(ciphertext):
    frequency = [0] * 26
    total_characters = 0
    clean_ciphertext = clean_text(ciphertext)
    for character in clean_ciphertext.lower():
        frequency[ord(character) - ord('a')] += 1
        total_characters += 1
    numerator = sum(n * (n - 1) for n in frequency) * 26
    denominator = total_characters * (total_characters - 1)
    return numerator / denominator


def fitness(ciphertext):
    current_fitness = 0
    clean_ciphertext = ''.join(str(character if character in string.ascii_lowercase else '')
                               for character in ciphertext.lower())
    for i in range(len(clean_ciphertext) - 3):
        current_tetragram = clean_ciphertext[i:i + 4]
        tetragram_index = sum(letter_to_index(current_tetragram[j]) * (26 ** (3 - j)) for j in range(4))
        frequency = tetragram_frequency[tetragram_index]
        if frequency == 0:
            current_fitness += -15
        else:
            current_fitness += math.log(frequency)
    current_fitness /= len(clean_ciphertext) - 3
    return current_fitness
