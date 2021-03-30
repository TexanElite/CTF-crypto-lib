import json

from .util import *


class RSA:

    def __init__(self, n, e, p=None, q=None, totient=None, d=None):
        self.n = n
        self.e = e
        self.p = p
        self.q = q
        self.totient = totient
        self.d = d

    def update(self):
        n_bits = len(bin(self.n)[2:])
        if self.p is None or self.q is None:
            if self.p is None and self.q is None:
                if n_bits <= 32:
                    factors = factorize(self.n)
                    if len(factors) != 2:
                        print("Error while updating values: n is not semiprime (n has more than 2 factors)")
                    else:
                        self.p = factors[0]
                        self.q = factors[1]
                else:
                    pass
            elif self.p is not None:
                self.q = self.n // self.p
            elif self.q is not None:
                self.p = self.n // self.q
        if self.p and self.q:
            self.totient = (self.p - 1) * (self.q - 1)
            self.d = mod_inverse(self.e, self.totient)

    def encrypt_message(self, pt):
        if type(pt) is str:
            pt = pt.encode('utf-8')
        pt = bytes_to_long(pt)
        ct = pow(pt, self.e, self.n)
        ct = long_to_bytes(ct)
        return ct

    def decrypt_message(self, ct):
        if self.d is None:
            print("Error while decrypting message: d is not defined")
            return
        if type(ct) is str:
            ct = ct.encode('utf-8')
        ct = bytes_to_long(ct)
        pt = pow(ct, self.d, self.n)
        pt = long_to_bytes(pt)
        return pt

    def __repr__(self):
        dict_form = {'n': self.n, 'e': self.e, 'p': self.p, 'q': self.q, 'totient': self.totient, 'd': self.d}
        return json.dumps(dict_form)
