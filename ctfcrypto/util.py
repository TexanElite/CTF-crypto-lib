import math


def factorize(n):
    return trial_division_factorizer(n)


def trial_division_factorizer(n):
    factors = []

    while n % 2 == 0:
        factors.append(2)
        n /= 2

    cur_divisor = 3

    while cur_divisor ** 2 <= n:
        while n % cur_divisor == 0:
            factors.append(cur_divisor)
            n //= cur_divisor
        cur_divisor += 2

    if n != 1:
        factors.append(n)

    return factors


def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)


def extended_gcd(a, b):
    r0, s0, t0 = a, 1, 0
    r1, s1, t1 = b, 0, 1

    while r1 != 0:
        q = r0 // r1
        r2 = r0 % r1

        s2 = s0 - q * s1
        t2 = t0 - q * t1

        r0, s0, t0 = r1, s1, t1
        r1, s1, t1 = r2, s2, t2
    return r0, s0, t0


def mod_inverse(n, mod):
    return (extended_gcd(n, mod)[1] + mod) % mod


def bytes_to_long(b):
    return int.from_bytes(b, 'big')


def long_to_bytes(n: int):
    return n.to_bytes((n.bit_length() + 7) // 8, 'big')
