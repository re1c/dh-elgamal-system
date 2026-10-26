"""
diffie_hellman.py
Implementasi Protokol Pertukaran Kunci Diffie-Hellman
Kelompok 17 - Kriptografi (A)
"""

import random
from crypto_core import (
    find_primitive_root,
    generate_prime,
    is_prime,
    is_primitive_root,
    mod_pow,
)


def generate_dh_parameters(min_val: int = 250, max_val: int = 5000) -> dict:
    """Membangkitkan pasangan parameter publik (n, g) yang valid.
    n: bilangan prima modulus.
    g: akar primitif (generator) dari n.
    """
    n = generate_prime(min_val, max_val)
    g = find_primitive_root(n)
    return {"n": n, "g": g}


def validate_dh_parameters(n: int, g: int) -> tuple[bool, str]:
    """Validasi matematis parameter publik Diffie-Hellman."""
    if not is_prime(n):
        return False, f"Modulus n={n} bukan bilangan prima."
    if not (1 < g < n):
        return False, f"Generator g harus berada pada rentang 1 < g < {n}."
    if not is_primitive_root(g, n):
        return False, f"Nilai g={g} bukan akar primitif dari n={n}."
    return True, "Parameter publik valid."


def generate_dh_private_key(n: int) -> int:
    """Membangkitkan kunci privat acak dalam rentang 1 < private_key < n - 1."""
    return random.randint(2, n - 2)


def compute_dh_public_key(g: int, private_key: int, n: int) -> int:
    """Menghitung kunci publik: Public = (g^private) mod n."""
    if not (1 < private_key < n - 1):
        raise ValueError(f"Kunci privat harus berada dalam rentang 1 < private < {n - 1}.")
    return mod_pow(g, private_key, n)


def compute_dh_shared_secret(peer_public_key: int, my_private_key: int, n: int) -> int:
    """Menghitung kunci sesi bersama: Shared = (PeerPublic^MyPrivate) mod n."""
    if not (0 < peer_public_key < n):
        raise ValueError("Kunci publik lawan bicara berada di luar rentang modulus.")
    return mod_pow(peer_public_key, my_private_key, n)
