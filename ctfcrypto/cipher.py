import string
import math
import os

letter_frequency = [.082, .015, .028, .043, .13, .022, .02, .061, .07, .0015, .0077, .04, .024, .067, .075, .019,
                    .00095, .06, .063, .091, .028, .0098, .024, .0015, .02, .00074]

tetragram_frequency = []


# Generating letter and tetragram frequencies:
def generate_frequencies():
    global letter_frequency
    global tetragram_frequency

    book_file_names = ['plato-republic', 'hawthorne-scarlet-letter', 'dickens-tale-of-two-cities',
                       'douglass-narrative-of-the-life-of-frederick-douglass']

    letter_frequency = [0] * 26
    tetragram_frequency = [0] * (26 ** 4)

    total_characters = 0
    total_tetragrams = 0

    for book_file_name in book_file_names:
        book = open(os.path.relpath('data/' + book_file_name + '.txt'), 'r')
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


def clean_text(text):
    return ''.join(str(character if character in string.ascii_lowercase else '')
                   for character in text.lower())


def letter_to_index(character):
    if character in string.ascii_lowercase:
        return ord(character) - ord('a')
    elif character in string.ascii_uppercase:
        return ord(character) - ord('A')
    return None


def shift_character(character, shift):
    if character in string.ascii_lowercase:
        shifted_character = chr((letter_to_index(character) + shift + 26) % 26 + ord('a'))
        return shifted_character
    elif character in string.ascii_uppercase:
        shifted_character = chr((letter_to_index(character) + shift + 26) % 26 + ord('A'))
        return shifted_character
    else:
        return character


def letter_frequency_cost(sequence):
    clean_sequence = clean_text(sequence)
    total_letters = len(clean_sequence)
    frequency = [(clean_sequence.lower().count(chr(ord('a') + i))) / total_letters for i in range(26)]
    cost = sum(abs(frequency[i] - letter_frequency[i]) for i in range(26))
    return cost / 2


class CaesarCipher:

    def __init__(self, shift):
        self.shift = (shift + max(0, shift // -26 + 1) * 26) % 26

    def encrypt(self, plaintext):
        ciphertext = ''
        for character in plaintext:
            ciphertext += shift_character(character, self.shift)
        return ciphertext

    def decrypt(self, ciphertext):
        unshift = 26 - self.shift
        plaintext = ''
        for character in ciphertext:
            plaintext += shift_character(character, unshift)
        return plaintext

    @classmethod
    def all_shifts(cls, message):
        return [(k, cls(k).encrypt(message)) for k in range(26)]

    @classmethod
    def solve(cls, ciphertext):
        return cls.analysis(ciphertext)[0][1:]

    @classmethod
    def analysis(cls, ciphertext):
        shifts = CaesarCipher.all_shifts(ciphertext)
        total_letters = sum(int(character in string.ascii_letters) for character in ciphertext)
        costs = [(letter_frequency_cost(cur_sequence[1]), cur_sequence[0], cur_sequence[1]) for cur_sequence in shifts]
        return sorted(costs)


class SubstitutionCipher:

    def __init__(self, key):
        self.key = {chr(ord('a') + i): key.lower()[i] for i in range(26)}
        self.key.update({chr(ord('A') + i): key.upper()[i] for i in range(26)})
        self.inverse_key = {self.key[k]: k for k in self.key}

    def encrypt(self, plaintext):
        ciphertext = ''
        for character in plaintext:
            if character not in self.key:
                ciphertext += character
            else:
                ciphertext += self.key[character]
        return ciphertext

    def decrypt(self, ciphertext):
        plaintext = ''
        for character in ciphertext:
            if character not in self.inverse_key:
                plaintext += character
            else:
                plaintext += self.inverse_key[character]
        return plaintext


class VigenereCipher:

    def __init__(self, key):
        self.key = key.lower()

    def encrypt(self, plaintext):
        ciphertext = ''
        idx = 0
        for character in plaintext:
            shift = letter_to_index(self.key[idx % len(self.key)])
            if character in string.ascii_letters:
                ciphertext += shift_character(character, shift)
                idx += 1
            else:
                ciphertext += character
        return ciphertext

    def decrypt(self, ciphertext):
        plaintext = ''
        idx = 0
        for character in ciphertext:
            unshift = 26 - letter_to_index(self.key[idx % len(self.key)])
            if character in string.ascii_letters:
                plaintext += shift_character(character, unshift)
                idx += 1
            else:
                plaintext += character
        return plaintext

    @classmethod
    def solve(cls, ciphertext, key_length=None):
        clean_ciphertext = clean_text(ciphertext)
        if key_length is None:
            key_length = cls.find_key_length(clean_ciphertext)
            if key_length is None:
                print('Error: could not guess key length')
                return None
        period = key_length
        parts = [''.join(clean_ciphertext[j] for j in range(i, len(clean_ciphertext), period)) for i in
                 range(period)]
        if period <= 4:
            return cls.brute_force_key(clean_ciphertext, '', period)
        else:
            print('Error: key length too large to brute force')

    @classmethod
    def brute_force_key(cls, ciphertext, key, depth):
        if depth == 0:
            if cls.fitness(cls(key).decrypt(ciphertext)) > -9.6:
                return [key]
            else:
                return []
        else:
            cur = []
            for character in string.ascii_lowercase:
                cur += cls.brute_force_key(ciphertext, key + character, depth - 1)
            return cur

    @classmethod
    def fitness(cls, ciphertext):
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

    @classmethod
    def index_of_coincidence(cls, ciphertext):
        frequency = [0] * 26
        total_characters = 0
        clean_ciphertext = clean_text(ciphertext)
        for character in clean_ciphertext.lower():
            frequency[ord(character) - ord('a')] += 1
            total_characters += 1
        numerator = sum(n * (n - 1) for n in frequency) * 26
        denominator = total_characters * (total_characters - 1)
        return numerator / denominator

    @classmethod
    def find_key_length(cls, ciphertext):
        period = 1
        found = False
        clean_ciphertext = clean_text(ciphertext)
        while not found and period <= len(clean_ciphertext):
            parts = [''.join(clean_ciphertext[j] for j in range(i, len(clean_ciphertext), period)) for i in
                     range(period)]
            cur_sum = sum(cls.index_of_coincidence(part) for part in parts)
            cum_ioc = cur_sum / period
            if cum_ioc >= 1.6:
                found = True
            else:
                period += 1
        if found:
            return period
        return None


generate_frequencies()
