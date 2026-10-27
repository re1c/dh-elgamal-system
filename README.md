# Diffie-Hellman Key Exchange and ElGamal Cryptosystem

Implementasi mandiri protokol pertukaran kunci Diffie-Hellman dan kriptosistem asimetris ElGamal berbasis persoalan Logaritma Diskrit (*Discrete Logarithm Problem*), tanpa dependensi pustaka kriptografi pihak ketiga.

Proyek ini disusun untuk memenuhi Tugas Mata Kuliah Kriptografi (A), Institut Teknologi Sepuluh Nopember.

## Kelompok 17
* Naswan Nashir Ramadhan (5025231246)
* Alfianz Risqia Ilahi Loven Kary (5025241164)
* Az Zahrra Tasya Adelia (5027241087)

---

## Arsitektur Sistem

Sistem dibangun secara modular dengan memisahkan komputasi matematika murni, logika protokol, pengujian otomatis, dan antarmuka interaktif:

```
dh-elgamal-system/
├── crypto_core.py        # Primitif matematika (is_prime, mod_pow, ext_gcd, primitive_root)
├── diffie_hellman.py     # Protokol Diffie-Hellman & penurunan kunci bersama
├── elgamal.py            # Kriptosistem ElGamal (Keygen, Encoding Kuliah/UTF-8, Enkripsi, Dekripsi)
├── app.py                # Dashboard web Streamlit interaktif
├── tests/                # Pengujian unit test otomatis (12 skenario pengujian)
│   ├── test_crypto_core.py
│   ├── test_diffie_hellman.py
│   └── test_elgamal.py
├── Laporan/              # Naskah laporan teknis berbasis Typst
├── requirements.txt      # Dependensi pustaka dasar
└── pytest.ini            # Konfigurasi pengujian pytest
```

---

## Prinsip dan Alur Matematis

### 1. Diffie-Hellman Key Exchange (DHKE)
* **Parameter Publik**: Bilangan prima modulus $n$ dan generator $g$ yang merupakan akar primitif dari $n$.
* **Pertukaran Kunci**:
  * Alice memilih kunci privat $x$ ($1 < x < n-1$) dan mengirim $X = g^x \bmod n$.
  * Bob memilih kunci privat $y$ ($1 < y < n-1$) dan mengirim $Y = g^y \bmod n$.
* **Kunci Sesi Bersama**:
  * Alice menghitung: $K = Y^x \bmod n = (g^y)^x \bmod n = g^{xy} \bmod n$.
  * Bob menghitung: $K' = X^y \bmod n = (g^x)^y \bmod n = g^{xy} \bmod n$.
  * Diperoleh nilai kunci identik $K = K'$ tanpa pernah mengirimkan nilai rahasia melalui saluran komunikasi.

### 2. Kriptosistem ElGamal
* **Pembangkitan Kunci**:
  * Penerima memilih prima $p$ dan akar primitif $g$, serta kunci privat acak $x$ ($1 < x < p-1$).
  * Kunci publik dihitung sebagai $y = g^x \bmod p$. Kunci publik adalah $(y, g, p)$.
* **Enkripsi**:
  * Pesan dipecah menjadi blok integer $m_i < p$.
  * Untuk tiap blok, pengirim memilih nilai acak $k$ ($1 < k < p-1$).
  * Ciphertext berupa pasangan $(a, b)$ dengan rumus:
    $$a = g^k \bmod p \qquad b = (y^k \cdot m_i) \bmod p$$
* **Dekripsi**:
  * Menggunakan Teorema Kecil Fermat untuk memulihkan $m_i$:
    $$m_i = b \cdot (a^x)^{-1} \equiv b \cdot a^{p - 1 - x} \pmod p$$

---

## Panduan Penggunaan

### 1. Persiapan Lingkungan Virtual
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Menjalankan Pengujian Otomatis
```bash
pytest -v
```

### 3. Menjalankan Dashboard Web Interaktif
```bash
streamlit run app.py
```
