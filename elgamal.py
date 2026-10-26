"""
elgamal.py
Implementasi Kriptosistem Kunci Publik ElGamal
Mendukung Mode Perkuliahan (A=00..Z=25) dan Mode Standar UTF-8
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


def generate_elgamal_keypair(p: int, g: int, preferred_x: int = None) -> dict:
    """Membangkitkan pasangan kunci ElGamal:
    Kunci Privat: x (dengan 1 < x < p - 1)
    Kunci Publik: (y, g, p) dengan y = (g^x) mod p
    """
    if not is_prime(p):
        raise ValueError(f"Nilai p={p} harus berupa bilangan prima.")
    if not is_primitive_root(g, p):
        raise ValueError(f"Nilai g={g} bukan akar primitif dari p={p}.")

    if preferred_x is not None:
        if not (1 < preferred_x < p - 1):
            raise ValueError(f"Kunci privat x harus berada pada rentang 1 < x < {p - 1}.")
        x = preferred_x
    else:
        x = random.randint(2, p - 2)

    y = mod_pow(g, x, p)

    return {
        "p": p,
        "g": g,
        "x": x,
        "y": y,
        "public_key": (y, g, p),
    }


# ----------------------------------------------------------------------------
# Mode 1: Encoding Slide Kuliah (A=00 .. Z=25)
# ----------------------------------------------------------------------------
def text_to_lecture_blocks(
    text: str, p: int, block_digits: int = None
) -> tuple[list[int], int, str]:
    """Konversi teks alfabet ke deret angka 2 digit dan pemecahan blok desimal m_i < p.
    Mengikuti format materi perkuliahan (A=00, B=01, ..., Z=25).
    """
    cleaned = "".join(c.upper() for c in text if c.isalpha())
    if not cleaned:
        raise ValueError("Teks minimal memuat satu karakter alfabet A-Z.")

    num_str = "".join(f"{ord(c) - ord('A'):02d}" for c in cleaned)

    if block_digits is not None:
        if block_digits % 2 != 0:
            raise ValueError("block_digits harus berupa bilangan genap.")
    else:
        # Tentukan kapasitas digit genap per blok (2, 4, ...) yang memenuhi seluruh m_i < p
        max_even = max(2, (len(str(p - 1)) // 2) * 2)
        block_digits = 2
        for candidate in range(max_even, 1, -2):
            chunks = [
                int(num_str[i : i + candidate])
                for i in range(0, len(num_str), candidate)
            ]
            if all(m < p for m in chunks):
                block_digits = candidate
                break

    # Pastikan panjang karakter sesuai kelipatan blok (padding 'X' jika ganjil)
    chars_per_block = block_digits // 2
    if len(cleaned) % chars_per_block != 0:
        pad_count = chars_per_block - (len(cleaned) % chars_per_block)
        cleaned += "X" * pad_count
        num_str = "".join(f"{ord(c) - ord('A'):02d}" for c in cleaned)

    blocks = []
    for i in range(0, len(num_str), block_digits):
        chunk = num_str[i : i + block_digits]
        blocks.append(int(chunk))

    return blocks, block_digits, num_str


def lecture_blocks_to_text(blocks: list[int], block_digits: int) -> str:
    """Rekonstruksi blok desimal menjadi teks alfabet asli."""
    full_str = "".join(f"{b:0{block_digits}d}" for b in blocks)
    chars = []
    for i in range(0, len(full_str), 2):
        pair = full_str[i : i + 2]
        if len(pair) == 2:
            val = int(pair)
            if 0 <= val <= 25:
                chars.append(chr(ord("A") + val))
    return "".join(chars)


# ----------------------------------------------------------------------------
# Mode 2: Encoding Standar UTF-8 (Biner / Teks Umum)
# ----------------------------------------------------------------------------
def text_to_utf8_blocks(text: str, p: int) -> tuple[list[int], int]:
    """Partisi teks UTF-8 ke dalam deretan integer m_i < p menggunakan Big-Endian."""
    raw_bytes = text.encode("utf-8")
    chunk_size = max(1, (p.bit_length() - 1) // 8)

    blocks = []
    for i in range(0, len(raw_bytes), chunk_size):
        chunk = raw_bytes[i : i + chunk_size]
        blocks.append(int.from_bytes(chunk, byteorder="big"))

    return blocks, chunk_size


def utf8_blocks_to_text(blocks: list[int], chunk_size: int) -> str:
    """Rekonstruksi deretan integer m_i menjadi string teks UTF-8."""
    reconstructed = bytearray()
    for m in blocks:
        byte_len = max(1, (m.bit_length() + 7) // 8)
        reconstructed.extend(m.to_bytes(byte_len, byteorder="big"))
    return bytes(reconstructed).decode("utf-8", errors="replace")


# ----------------------------------------------------------------------------
# Operasi Enkripsi & Dekripsi
# ----------------------------------------------------------------------------
def encrypt_elgamal_blocks(
    blocks: list[int],
    y: int,
    g: int,
    p: int,
    custom_k_list: list[int] = None,
) -> list[dict]:
    """Enkripsi blok integer m_i menghasilkan pasangan (a, b):
    a = (g^k) mod p
    b = (y^k * m) mod p
    """
    records = []
    for idx, m in enumerate(blocks):
        if not (0 <= m < p):
            raise ValueError(f"Blok pesan m={m} melebihi rentang modulus p={p}.")

        if custom_k_list and idx < len(custom_k_list):
            k = custom_k_list[idx]
        else:
            k = random.randint(2, p - 2)

        a = mod_pow(g, k, p)
        yk = mod_pow(y, k, p)
        b = (yk * m) % p

        records.append({
            "block_index": idx + 1,
            "m": m,
            "k": k,
            "a": a,
            "b": b,
            "pair": (a, b),
        })
    return records


def decrypt_elgamal_blocks(
    cipher_pairs: list[tuple[int, int]],
    x: int,
    p: int,
) -> list[dict]:
    """Dekripsi pasangan (a, b) menggunakan Teorema Kecil Fermat:
    m = (b * a^(p - 1 - x)) mod p
    """
    records = []
    fermat_exp = p - 1 - x

    for idx, (a, b) in enumerate(cipher_pairs):
        ax_inv = mod_pow(a, fermat_exp, p)
        m = (b * ax_inv) % p

        records.append({
            "block_index": idx + 1,
            "a": a,
            "b": b,
            "ax_inv": ax_inv,
            "m": m,
        })
    return records
