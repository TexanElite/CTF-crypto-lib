from .frequency import *
from .util import *


def shift_character(character, shift):
    if character in string.ascii_lowercase:
        shifted_character = chr((letter_to_index(character) + shift + 26) % 26 + ord('a'))
        return shifted_character
    elif character in string.ascii_uppercase:
        shifted_character = chr((letter_to_index(character) + shift + 26) % 26 + ord('A'))
        return shifted_character
    else:
        return character


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
        costs = [(letter_frequency_cost(cur_sequence[1]), (26 - cur_sequence[0]) % 26, cur_sequence[1]) for cur_sequence in shifts]
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
            keys = cls.brute_force_key(clean_ciphertext, '', period)
            return [(key, VigenereCipher(key).decrypt(ciphertext)) for key in keys]
        else:
            print('Error: key length too large to brute force')

    @classmethod
    def brute_force_key(cls, ciphertext, key, depth):
        if depth == 0:
            if fitness(cls(key).decrypt(ciphertext)) > -11:
                return [key]
            else:
                return []
        else:
            cur = []
            for character in string.ascii_lowercase:
                cur += cls.brute_force_key(ciphertext, key + character, depth - 1)
            return cur

    @classmethod
    def find_key_length(cls, ciphertext):
        period = 1
        found = False
        clean_ciphertext = clean_text(ciphertext)
        while not found and period <= len(clean_ciphertext):
            parts = [''.join(clean_ciphertext[j] for j in range(i, len(clean_ciphertext), period)) for i in
                     range(period)]
            cur_sum = sum(index_of_coincidence(part) for part in parts)
            cum_ioc = cur_sum / period
            if cum_ioc >= 1.6:
                found = True
            else:
                period += 1
        if found:
            return period
        return None


load_frequencies()
