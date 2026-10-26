"""
crypto_core.py
Modul Primitif Matematika Murni Diffie-Hellman dan ElGamal
Implementasi mandiri tanpa dependensi pustaka kriptografi eksternal.
"""

import random


def is_prime(num: int) -> bool:
    """Uji keprimaan bilangan bulat menggunakan metode Trial Division 6k +/- 1."""
    if num < 2:
        return False
    if num in (2, 3):
        return True
    if num % 2 == 0 or num % 3 == 0:
        return False
    i = 5
    while i * i <= num:
        if num % i == 0 or num % (i + 2) == 0:
            return False
        i += 6
    return True


def gcd(a: int, b: int) -> int:
    """Menghitung Pembagi Bersama Terbesar (PBB) dengan Algoritma Euclidean."""
    while b != 0:
        a, b = b, a % b
    return a


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    """
    Algoritma Euclidean Diperluas (Extended Euclidean Algorithm).
    Menghasilkan tuple (gcd, x, y) yang memenuhi: a*x + b*y = gcd(a, b).
    """
    if a == 0:
        return b, 0, 1
    g, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return g, x, y


def mod_inverse(a: int, m: int) -> int:
    """
    Menghitung invers perkalian modular a^-1 mod m.
    Memastikan (a * x) % m == 1.
    """
    g, x, _ = extended_gcd(a % m, m)
    if g != 1:
        raise ValueError(f"Invers modular tidak ditemukan karena gcd({a}, {m}) != 1.")
    return x % m


def mod_pow(base: int, exp: int, mod: int) -> int:
    """
    Perpangkatan modular manual menggunakan algoritma Square-and-Multiply.
    Menghitung (base^exp) % mod tanpa risiko memory overflow.
    """
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp //= 2
    return result


def get_prime_factors(n: int) -> set[int]:
    """Mencari seluruh faktor prima unik dari bilangan n."""
    factors = set()
    d = 2
    temp = n
    while d * d <= temp:
        if temp % d == 0:
            factors.add(d)
            while temp % d == 0:
                temp //= d
        d += 1
    if temp > 1:
        factors.add(temp)
    return factors


def is_primitive_root(g: int, p: int) -> bool:
    """
    Validasi akar primitif g modulo prima p.
    Memeriksa syarat: g^((p-1)/q) mod p != 1 untuk setiap faktor prima q dari (p - 1).
    """
    if not is_prime(p):
        return False
    if not (1 < g < p):
        return False

    totient = p - 1
    factors = get_prime_factors(totient)

    for q in factors:
        if mod_pow(g, totient // q, p) == 1:
            return False
    return True


def find_primitive_root(p: int) -> int:
    """Mencari akar primitif terkecil untuk bilangan prima p."""
    if not is_prime(p):
        raise ValueError(f"p={p} bukan bilangan prima.")
    for candidate in range(2, p):
        if is_primitive_root(candidate, p):
            return candidate
    raise ValueError(f"Akar primitif tidak ditemukan untuk p={p}.")


def generate_prime(min_val: int = 1000, max_val: int = 5000) -> int:
    """Membangkitkan bilangan prima acak dalam rentang yang ditentukan."""
    while True:
        candidate = random.randrange(min_val | 1, max_val, 2)
        if is_prime(candidate):
            return candidate
