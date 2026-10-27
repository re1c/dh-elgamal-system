"""
test_elgamal.py
Pengujian unit test kriptosistem ElGamal
"""

import pytest
from elgamal import (
    decrypt_elgamal_blocks,
    encrypt_elgamal_blocks,
    generate_elgamal_keypair,
    lecture_blocks_to_text,
    text_to_lecture_blocks,
    text_to_utf8_blocks,
    utf8_blocks_to_text,
)


def test_elgamal_slide_halo_example():
    p = 2273
    g = 3
    x = 243

    keypair = generate_elgamal_keypair(p, g, preferred_x=x)
    assert keypair["y"] == 461

    blocks, block_digits, _, pad_count = text_to_lecture_blocks("HALO", p)
    assert blocks == [700, 1114]
    assert block_digits == 4
    assert pad_count == 0

    enc_records = encrypt_elgamal_blocks(
        blocks, keypair["y"], g, p, custom_k_list=[1463, 2001]
    )
    assert enc_records[0]["a"] == 1439
    assert enc_records[0]["b"] == 74
    assert enc_records[1]["a"] == 1220
    assert enc_records[1]["b"] == 1682

    cipher_pairs = [(r["a"], r["b"]) for r in enc_records]
    dec_records = decrypt_elgamal_blocks(cipher_pairs, x, p)
    assert dec_records[0]["ax_inv"] == 1791
    assert dec_records[0]["m"] == 700
    assert dec_records[1]["ax_inv"] == 1125
    assert dec_records[1]["m"] == 1114

    recovered = lecture_blocks_to_text([d["m"] for d in dec_records], block_digits, pad_count)
    assert recovered == "HALO"


def test_elgamal_lecture_padding():
    p = 3319
    g = 6
    keypair = generate_elgamal_keypair(p, g)

    blocks, block_digits, _, pad_count = text_to_lecture_blocks("LOGARITMA", p)
    assert pad_count == 1

    enc_records = encrypt_elgamal_blocks(blocks, keypair["y"], g, p)
    cipher_pairs = [(r["a"], r["b"]) for r in enc_records]

    dec_records = decrypt_elgamal_blocks(cipher_pairs, keypair["x"], p)
    recovered = lecture_blocks_to_text(
        [d["m"] for d in dec_records], block_digits, pad_count
    )

    assert recovered == "LOGARITMA"


def test_elgamal_utf8_mode():
    p = 2273
    g = 3
    keypair = generate_elgamal_keypair(p, g)

    original_text = "Aku suka kriptografi. Diffie-Hellman & ElGamal 2026!"
    blocks, chunk_size = text_to_utf8_blocks(original_text, p)

    enc_records = encrypt_elgamal_blocks(blocks, keypair["y"], g, p)
    cipher_pairs = [(r["a"], r["b"]) for r in enc_records]

    dec_records = decrypt_elgamal_blocks(cipher_pairs, keypair["x"], p)
    recovered = utf8_blocks_to_text([d["m"] for d in dec_records], chunk_size)

    assert recovered == original_text
