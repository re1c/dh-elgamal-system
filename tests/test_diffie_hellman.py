"""
test_diffie_hellman.py
Pengujian unit test protokol pertukaran kunci Diffie-Hellman
"""

import pytest
from diffie_hellman import (
    compute_dh_public_key,
    compute_dh_shared_secret,
    generate_dh_parameters,
    generate_dh_private_key,
    validate_dh_parameters,
)


def test_dh_slide_example():
    # Validasi numerik persis slide kuliah
    n = 251
    g = 6
    x = 124
    y = 158

    is_valid, _ = validate_dh_parameters(n, g)
    assert is_valid is True

    # Kunci publik Alice (X) dan Bob (Y)
    X = compute_dh_public_key(g, x, n)
    Y = compute_dh_public_key(g, y, n)
    assert X == 209
    assert Y == 197

    # Kunci sesi bersama
    K_alice = compute_dh_shared_secret(Y, x, n)
    K_bob = compute_dh_shared_secret(X, y, n)
    assert K_alice == 79
    assert K_bob == 79
    assert K_alice == K_bob


def test_dh_random_flow():
    params = generate_dh_parameters(200, 1000)
    n, g = params["n"], params["g"]

    x = generate_dh_private_key(n)
    y = generate_dh_private_key(n)

    X = compute_dh_public_key(g, x, n)
    Y = compute_dh_public_key(g, y, n)

    K_alice = compute_dh_shared_secret(Y, x, n)
    K_bob = compute_dh_shared_secret(X, y, n)

    assert K_alice == K_bob
    assert 0 < K_alice < n
