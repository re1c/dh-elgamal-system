"""
test_crypto_core.py
Pengujian unit test untuk fungsi primitif matematika
"""

import pytest
from crypto_core import (
    is_prime,
    gcd,
    extended_gcd,
    mod_inverse,
    mod_pow,
    get_prime_factors,
    is_primitive_root,
    find_primitive_root,
    generate_prime,
)


def test_is_prime():
    assert is_prime(-5) is False
    assert is_prime(0) is False
    assert is_prime(1) is False
    assert is_prime(2) is True
    assert is_prime(3) is True
    assert is_prime(7) is True
    assert is_prime(251) is True
    assert is_prime(2273) is True
    assert is_prime(4) is False
    assert is_prime(9) is False


def test_gcd_and_extended_gcd():
    assert gcd(48, 18) == 6
    g, x, y = extended_gcd(30, 20)
    assert g == 10
    assert 30 * x + 20 * y == 10


def test_mod_inverse():
    # 3 * x = 1 mod 7 -> x = 5 (karena 15 mod 7 = 1)
    assert mod_inverse(3, 7) == 5
    with pytest.raises(ValueError):
        mod_inverse(4, 8)


def test_mod_pow():
    # Sesuai contoh slide: 6^124 mod 251 = 209
    assert mod_pow(6, 124, 251) == 209
    # 3^243 mod 2273 = 461
    assert mod_pow(3, 243, 2273) == 461


def test_primitive_root_validation():
    # Sesuai slide kuliah:
    # Pada p = 7: g = 3 adalah akar primitif, sedangkan g = 2 bukan
    assert is_primitive_root(3, 7) is True
    assert is_primitive_root(2, 7) is False

    # Pada p = 251: g = 6 adalah akar primitif
    assert is_primitive_root(6, 251) is True

    # Pada p = 2273: g = 3 adalah akar primitif
    assert is_primitive_root(3, 2273) is True


def test_find_primitive_root():
    assert find_primitive_root(7) == 3


def test_generate_prime():
    p = generate_prime(500, 1500)
    assert is_prime(p) is True
    assert 500 <= p <= 1500
