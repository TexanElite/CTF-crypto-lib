import string

letter_frequency = [.082, .015, .028, .043, .13, .022, .02, .061, .07, .0015, .0077, .04, .024, .067, .075, .019,
                    .00095, .06, .063, .091, .028, .0098, .024, .0015, .02, .00074]


class CaesarCipher:

    def __init__(self, shift):
        self.shift = (shift + max(0, shift // -26 + 1) * 26) % 26

    def encrypt(self, plaintext):
        self.shift %= 26
        ciphertext = ''
        for character in plaintext:
            if character in string.ascii_lowercase:
                shifted_character = chr((ord(character) - ord('a') + self.shift + 26) % 26 + ord('a'))
                ciphertext += shifted_character
            elif character in string.ascii_uppercase:
                shifted_character = chr((ord(character) - ord('A') + self.shift + 26) % 26 + ord('A'))
                ciphertext += shifted_character
            else:
                ciphertext += character
        return ciphertext

    def decrypt(self, ciphertext):
        unshift = (26 - self.shift) % 26
        plaintext = ''
        for character in ciphertext:
            if character in string.ascii_lowercase:
                shifted_character = chr((ord(character) - ord('a') + unshift + 26) % 26 + ord('a'))
                plaintext += shifted_character
            elif character in string.ascii_uppercase:
                shifted_character = chr((ord(character) - ord('A') + unshift + 26) % 26 + ord('A'))
                plaintext += shifted_character
            else:
                plaintext += character
        return plaintext

    @classmethod
    def all_shifts(cls, message):
        return [(k, cls(k).encrypt(message)) for k in range(26)]

    @classmethod
    def analysis(cls, ciphertext):
        shifts = CaesarCipher.all_shifts(ciphertext)
        total_letters = sum(int(character in string.ascii_letters) for character in ciphertext)
        frequencies = [
            [(sequence.count(chr(ord('a') + i)) + sequence.count(chr(ord('A') + i))) / total_letters for i in range(26)]
            for _, sequence in shifts]
        costs = [(sum((frequencies[cur_sequence][i] - letter_frequency[i]) ** 2 for i in range(26)),
                  shifts[cur_sequence][1], cur_sequence) for cur_sequence in range(26)]
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
    """TODO: Implementation"""
    pass
