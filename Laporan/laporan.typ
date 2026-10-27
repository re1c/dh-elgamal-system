#set page(
  paper: "a4",
  margin: (top: 2.5cm, bottom: 2.5cm, left: 3cm, right: 2.5cm),
  header: context {
    if here().page() > 1 [
      #grid(
        columns: (1fr, auto),
        align: (left, right),
        text(size: 8.5pt, fill: luma(110))[Laporan Tugas Kriptografi: Diffie-Hellman & ElGamal],
        text(size: 8.5pt, fill: luma(110))[Kelompok 17]
      )
      #v(-0.4em)
      #line(length: 100%, stroke: 0.4pt + luma(180))
    ]
  },
  footer: context {
    if here().page() > 1 [
      #line(length: 100%, stroke: 0.4pt + luma(180))
      #v(-0.2em)
      #align(center, text(size: 9pt)[#here().page()])
    ]
  }
)

#set text(font: ("Times New Roman", "Liberation Serif"), size: 10.5pt, lang: "id")
#set par(justify: true, leading: 0.78em, first-line-indent: 1.5em)
#set heading(numbering: "1.1")

#show raw.where(block: true): block.with(
  fill: luma(248),
  inset: (x: 10pt, y: 8pt),
  radius: 4pt,
  stroke: 0.5pt + luma(200),
  width: 100%,
)
#show raw: set text(font: ("Liberation Mono", "DejaVu Sans Mono"), size: 8.5pt)

#let mod = math.op("mod")
#let gcd = math.op("gcd")

// ============================================================================
// HALAMAN 1: IDENTITAS RESMI
// ============================================================================
#align(center)[
  #v(2cm)
  #text(size: 16pt, weight: "bold")[LAPORAN TUGAS PEMROGRAMAN KRIPTOGRAFI]\
  #v(0.4cm)
  #text(size: 13pt)[
    Implementasi Mandiri Protokol Pertukaran Kunci Diffie-Hellman\
    dan Kriptosistem Asimetris ElGamal Berbasis Logaritma Diskrit
  ]\
  #v(2.5cm)

  #text(size: 11pt)[Disusun oleh Kelompok 17 (Kelas A):]\
  #v(0.5cm)
  #align(center)[
    #table(
      columns: (auto, auto),
      stroke: none,
      align: (left, left),
      row-gutter: 0.8em,
      column-gutter: 2.5em,
      [Naswan Nashir Ramadhan], [(5025231246)],
      [Alfianz Risqia Ilahi Loven Kary], [(5025241164)],
      [Az Zahrra Tasya Adelia], [(5027241087)],
    )
  ]

  #v(1fr)

  #text(size: 11pt)[
    Mata Kuliah Kriptografi (A)\
    Institut Teknologi Sepuluh Nopember\
    Semester Ganjil 2026/2027
  ]
  #v(1cm)
]

#pagebreak()

// ============================================================================
// ISI LAPORAN
// ============================================================================

= Pendahuluan

== Latar Belakang
Keamanan transmisi data pada saluran komunikasi terbuka mengandalkan dua mekanisme utama, yaitu kesepakatan kunci simetris (_key establishment_) dan enkripsi pesan asimetris. Kriptografi kunci publik bertumpu pada fungsi matematika satu arah terperangkap (_trapdoor one-way function_). Di samping persoalan faktorisasi bilangan bulat besar pada RSA, pilar fundamental lainnya adalah Persoalan Logaritma Diskrit (_Discrete Logarithm Problem_ / DLP) pada grup siklik berhingga bilangan bulat modulo prima.

Protokol pertukaran kunci Diffie-Hellman (1976) memungkinkan dua pihak menurunkan kunci sesi simetris bersama tanpa perlu mengirimkan kunci rahasia tersebut melalui jaringan. Melanjutkan fondasi tersebut, Taher ElGamal (1984) memperluas pemanfaatan DLP untuk merancang skema enkripsi dan dekripsi pesan kunci publik yang bersifat probabilistik, di mana enkripsi pesan yang sama dengan kunci publik yang sama akan menghasilkan pasangan teks tersandi (_ciphertext_) yang berbeda karena penyertaan parameter acak pada setiap blok.

== Kriteria dan Batasan Penugasan
Implementasi sistem ini dirancang memenuhi batasan penugasan secara ketat:
- *Bebas Pustaka Kriptografi*: Seluruh operasi matematika teori bilangan dibangun murni dari dasar (_from scratch_) tanpa pustaka pihak ketiga.
- *Modularitas Fungsi*: Setiap tahapan operasional Diffie-Hellman dan ElGamal diisolasi ke dalam fungsi-fungsi independen yang transparan.
- *Verifikasi Materi Kuliah*: Menyediakan skenario pembuktian numerik yang mencocokkan contoh pada materi perkuliahan ke-9 secara identik, meliputi pertukaran kunci Diffie-Hellman ($n=251, g=6$) dan enkripsi ElGamal teks "HALO" ($p=2273, g=3$).
- *Kelengkapan Pengujian*: Memvalidasi seluruh fungsi menggunakan rangkaian pengujian otomatis (_unit test_) berbasis `pytest`.

= Landasan Teori dan Formulasi Matematis

== Grup Siklik dan Akar Primitif (Primitive Root)
Misalkan $p$ adalah bilangan prima. Berdasarkan fungsi totient Euler, banyaknya bilangan bulat positif yang relatif prima terhadap $p$ adalah $phi(p) = p - 1$. Bilangan bulat $g$ didefinisikan sebagai akar primitif (_generator_) modulo $p$ jika himpunan perpangkatan:
$ { g^1 mod p, quad g^2 mod p, quad dots, quad g^(p-1) mod p } $
menghasilkan permutasi seluruh elemen bilangan bulat tereduksi $\{1, 2, dots, p - 1\}$. Artinya, panjang siklus perpangkatan mencapai batas maksimum sepanjang $p - 1$.

Pemeriksaan akar primitif secara efisien tidak memerlukan pengujian ke seluruh $p - 1$ nilai eksponen. Nilai $g$ terbukti sebagai akar primitif sah dari $p$ jika dan hanya jika untuk setiap faktor prima unik $q$ dari $(p - 1)$ berlaku:
$ g^((p - 1) / q) eq.not 1 quad (mod p) $

== Persoalan Logaritma Diskrit (Discrete Logarithm Problem)
Diberikan bilangan prima $p$, basis generator $g$, dan eksponen privat $x$, operasi perpangkatan modular:
$ y equiv g^x quad (mod p) $
dapat dihitung secara efisien menggunakan algoritma _Square-and-Multiply_ dengan kompleksitas waktu $O(log x)$.

Sebaliknya, jika hanya diketahui nilai publik $y, g,$ dan $p$, persoalan untuk memulihkan kembali nilai eksponen rahasia $x$ sedemikian sehingga $g^x equiv y space (mod p)$ disebut sebagai _Discrete Logarithm Problem_ (DLP). Belum ada algoritma klasik waktu polinomial yang mampu memecahkan persoalan ini untuk nilai prima $p$ yang berukuran besar.

== Protokol Diffie-Hellman Key Exchange (DHKE)
Protokol ini berjalan melalui tahapan aljabar berikut:
- *Parameter Publik*: Alice dan Bob menyepakati bilangan prima $n$ dan generator $g$. Nilai $(n, g)$ bersifat publik dan aman dipertukarkan di saluran terbuka.
- *Pembangkitan Kunci Privat*: Alice memilih bilangan acak rahasia $x$ ($1 < x < n - 1$), sedangkan Bob memilih bilangan acak rahasia $y$ ($1 < y < n - 1$).
- *Transmisi Kunci Publik*: Alice menghitung $X = g^x mod n$ dan mengirimkannya ke Bob. Bob menghitung $Y = g^y mod n$ dan mengirimkannya ke Alice.
- *Penurunan Kunci Sesi Bersama*: Alice menghitung $K = Y^x mod n$, sedangkan Bob menghitung $K' = X^y mod n$.

Sesuai sifat komutatif eksponensiasi modular:
$ K = (g^y)^x equiv g^(x y) equiv (g^x)^y = K' quad (mod n) $
Kunci sesi simetris $K = K'$ berhasil diperoleh kedua belah pihak tanpa membuka informasi nilai $x$ maupun $y$ kepada penyadap di saluran komunikasi.

== Kriptosistem Kunci Publik ElGamal
Skema ElGamal mencakup tiga prosedur utama:
- *Pembangkitan Kunci*: Penerima memilih prima $p$, akar primitif $g$, dan kunci privat acak $x$ ($1 < x < p - 1$). Kunci publik dihitung sebagai $y = g^x mod p$. Pasangan kunci publik penerima adalah $(y, g, p)$ dan kunci privatnya adalah $x$.
- *Enkripsi Pesan*: Pesan dipecah menjadi deret blok integer $m_i$ ($0 <= m_i < p$). Untuk tiap blok, pengirim memilih bilangan acak $k$ ($1 < k < p - 1$), lalu menghitung pasangan teks tersandi $(a, b)$:
  $ a = g^k mod p $
  $ b = (y^k dot m_i) mod p $
  Ukuran teks tersandi menjadi dua kali lipat ukuran teks asli karena setiap blok $m_i$ diwakili oleh pasangan nilai $(a, b)$.
- *Dekripsi Pesan*: Penerima memulihkan $m_i$ menggunakan kunci privat $x$ dengan memanfaatkan Teorema Kecil Fermat:
  $ (a^x)^(-1) equiv a^(p - 1 - x) quad (mod p) $
  $ m_i = (b dot a^(p - 1 - x)) mod p $

= Struktur Repositori dan Rancang Bangun Sistem

Arsitektur perangkat lunak disusun secara modular dengan memisahkan domain matematika murni, mesin protokol, antarmuka interaktif, dan pengujian otomatis:

#align(center)[
#table(
  columns: (1.5fr, 3.5fr),
  stroke: 0.5pt + luma(180),
  fill: (col, row) => if row == 0 { luma(240) } else { none },
  inset: 7pt,
  align: (left, left),
  [*Berkas / Modul*], [*Tanggung Jawab dan Fungsi Utama*],
  [`crypto_core.py`], [Primitif matematika murni independen: uji prima trial division, faktorisasi pembagi totient, verifikasi akar primitif, eksponensiasi Square-and-Multiply, dan invers modular.],
  [`diffie_hellman.py`], [Logika protokol pertukaran kunci: validasi parameter publik, kalkulasi kunci publik pihak berkomunikasi, dan derivasi kunci sesi bersama.],
  [`elgamal.py`], [Kriptosistem kunci publik ElGamal: pembentukan kunci, partisi blok desimal perkuliahan, partisi biner UTF-8, enkripsi pasangan blok, dan dekripsi modular Fermat.],
  [`app.py`], [Antarmuka web interaktif Streamlit: visualisasi saluran Alice-Bob, panel inspeksi penyadap pasif Eve, tabel proses enkripsi/dekripsi per blok, dan lab teori DLP.],
  [`tests/`], [Rangkaian 12 pengujian unit otomatis berbasis pytest untuk memverifikasi kebenaran matematis dan kompatibilitas contoh perkuliahan.]
)
]

= Penjelasan Fungsi Setiap Tahapan Program

== Modul Primitif Matematika Murni (`crypto_core.py`)
Modul ini menjadi fondasi seluruh kalkulasi aljabar tanpa dependensi eksternal:
- *Uji Keprimaan (`is_prime`)*: Mengimplementasikan _Trial Division_ teroptimasi $6k plus.minus 1$. Setelah memeriksa basis 2 dan 3, perulangan melompati seluruh bilangan genap dan kelipatan 3 hingga batas $sqrt(n)$, sehingga memangkas kompleksitas komputasi menjadi $O(sqrt(n))$.
- *Pembagi Bersama Terbesar (`gcd` & `extended_gcd`)*: Menggunakan Algoritma Euclidean untuk memeriksa keterbagian prima relatif, serta Algoritma Euclidean Diperluas untuk menghitung koefisien Bézout ($a dot x + b dot y = gcd(a, b)$).
- *Invers Perkalian Modular (`mod_inverse`)*: Menghitung nilai $a^(-1) mod m$ yang memenuhi $(a dot x) mod m = 1$ memanfaatkan koefisien $x$ dari Algoritma Euclidean Diperluas.
- *Eksponensiasi Biner Modular (`mod_pow`)*: Menghitung perpangkatan modular dengan algoritma _Square-and-Multiply_. Eksponen dipindai secara bitwise; basis dikuadratkan pada setiap langkah dan dikalikan dengan basis jika bit aktif bernilai 1. Algoritma ini berjalan dalam kompleksitas waktu $O(log "exp")$ dan mencegah luapan memori (_memory overflow_).
- *Verifikasi dan Pencarian Akar Primitif (`is_primitive_root` & `find_primitive_root`)*: Fungsi `get_prime_factors()` mengekstrak seluruh faktor prima dari $p - 1$. Fungsi `is_primitive_root()` memvalidasi syarat keterbagian generator, dan fungsi `find_primitive_root()` mencari generator terkecil secara iteratif.

== Tahapan Protokol Diffie-Hellman (`diffie_hellman.py`)
- *Tahap 1: Pembentukan Parameter Publik (`generate_dh_parameters` & `validate_dh_parameters`)*: Membangkitkan bilangan prima acak $n$ dan generator sah $g$, serta memvalidasi keabsahan parameter sebelum proses pertukaran dimulai.
- *Tahap 2: Pembangkitan Kunci Privat (`generate_dh_private_key`)*: Membangkitkan integer rahasia $x$ dan $y$ secara acak pada rentang $2 <= x, y <= n - 2$.
- *Tahap 3: Kalkulasi Kunci Publik (`compute_dh_public_key`)*: Mengeksekusi eksponensiasi modular publik $X = g^x mod n$ dan $Y = g^y mod n$ menggunakan fungsi `mod_pow()`.
- *Tahap 4: Penurunan Kunci Sesi Bersama (`compute_dh_shared_secret`)*: Menurunkan kunci sesi menggunakan kunci publik pihak lawan dan kunci privat sendiri: $K = Y^x mod n$ dan $K' = X^y mod n$.

== Tahapan Kriptosistem ElGamal (`elgamal.py`)
- *Tahap 1: Pembangkitan Kunci (`generate_elgamal_keypair`)*: Menerima parameter prima $p$ dan generator $g$. Menghasilkan kunci privat $x$ dan kunci publik $y = g^x mod p$.
- *Tahap 2: Pemecahan Blok Pesan (`text_to_lecture_blocks` & `text_to_utf8_blocks`)*:
  - Mode Kuliah: Memetakan alfabet ke dua digit angka ($A=00 dots Z=25$) lalu membaginya ke dalam blok 4-digit agar nilai $m_i < p$.
  - Mode UTF-8: Mengonversi teks ke deret biner lalu mempartisinya ke dalam integer Big-Endian berukuran aman terhadap panjang bit modulus $p$.
- *Tahap 3: Enkripsi Blok Pesan (`encrypt_elgamal_blocks`)*: Untuk setiap blok pesan $m_i$, dipilih nilai acak $k$, lalu dihitung $a = g^k mod p$ dan $b = (y^k dot m_i) mod p$.
- *Tahap 4: Dekripsi Blok Pesan (`decrypt_elgamal_blocks`)*: Memulihkan integer pesan $m_i$ via invers Teorema Kecil Fermat menggunakan eksponen $p - 1 - x$.
- *Tahap 5: Rekonstruksi Teks dan Pelepasan Padding (`lecture_blocks_to_text` & `utf8_blocks_to_text`)*: Mengonversi kembali integer pesan $m_i$ ke teks asli dan melepaskan karakter pengganjal (_padding_) secara presisi.

== Penanganan Blok Ganjil dan Padding Deterministik
Pada mode perkuliahan, pemetaan dua digit menghasilkan blok 4-digit (setara dua huruf per blok). Apabila teks masukan memiliki panjang ganjil (seperti kata "LOGARITMA" yang terdiri atas 9 huruf), huruf terakhir tidak dapat membentuk pasangan 4-digit secara utuh.

Sistem menerapkan penanganan bantalan (_padding_) berintegritas:
- Enkoder menyisipkan satu huruf pengganjal 'X' di akhir deretan sehingga panjang karakter genap (menjadi "LOGARITMAX" / 5 blok) dan menyimpan jumlah bantalan (`pad_count = 1`).
- Pada tahap dekripsi, setelah kelima blok dipulihkan secara matematis menjadi deretan karakter, fungsi pemulihan memotong sejumlah `pad_count` karakter dari posisi akhir. Teks kembali pulih menjadi "LOGARITMA", dan antarmuka memberikan catatan transparan mengenai pelepasan karakter pengganjal tersebut.

= Dokumentasi Antarmuka Web Interaktif (`app.py`)

Dashboard interaktif dibangun menggunakan Streamlit dengan tata letak visual multi-tab:

== Tab 1: Pertukaran Kunci Diffie-Hellman
- Menyediakan tombol preset materi perkuliahan ($n=251, g=6, x=124, y=158$) untuk demonstrasi instan, serta tombol acak parameter baru.
- Memisahkan visualisasi komputasi Sisi Alice dan Sisi Bob secara berdampingan.
- Menyediakan panel edukasi sudut pandang penyadap (Eve) yang menginspeksi nilai apa saja yang bocor ke saluran publik ($n, g, X, Y$) dan menjelaskan mengapa Eve tidak dapat memulihkan kunci sesi $K$ tanpa memecahkan persoalan logaritma diskrit.

== Tab 2: Kriptosistem ElGamal
- Mendukung dua skema pengodean: Mode Materi Kuliah ($A=00 dots Z=25$) dan Mode Teks Umum (UTF-8) untuk teks panjang, huruf kecil, dan simbol.
- Menyediakan tabel detail per blok yang menampilkan nilai integer $m$, nilai acak $k$, $a = g^k mod p$, $b = (y^k dot m) mod p$, dan pasangan teks tersandi $(a, b)$.
- Menampilkan tabel proses dekripsi per blok yang memverifikasi kalkulasi $a^(p-1-x) mod p$ hingga pesan asli pulih seutuhnya.
- Menggunakan mekanisme fungsi alih status (_callback_) yang secara otomatis membersihkan tabel komputasi lama saat pengguna beralih mode.

== Tab 3: Laboratorium Teori Akar Primitif & DLP
- *Uji Siklus Generator*: Menghitung dan menampilkan tabel perpangkatan $g^i mod p$ untuk membuktikan apakah nilai $g$ membentuk $p - 1$ elemen unik (akar primitif) atau mengalami siklus berulang sebelum mencapai $p - 1$.
- *Simulasi DLP*: Menyediakan penelusuran linier (_brute-force search_) untuk mencari nilai eksponen rahasia $x$ pada kongruensi $b equiv g^x quad (mod p)$, mendemonstrasikan kompleksitas komputasi pencarian logaritma diskrit.

= Pengujian dan Pembuktian Numerik

== Verifikasi Diffie-Hellman Sesuai Slide Perkuliahan
Pengujian mencocokkan perhitungan contoh slide pertemuan ke-9:
- Parameter Publik: $n = 251$ (prima), $g = 6$ (akar primitif sah dengan panjang siklus 250).
- Kunci Privat: Alice $x = 124$, Bob $y = 158$.
- Kunci Publik yang Ditransmisikan:
  $ X = 6^124 mod 251 = 209 $
  $ Y = 6^158 mod 251 = 197 $
- Derivasi Kunci Sesi Bersama:
  $ K_("Alice") = 197^124 mod 251 = 79 $
  $ K'_("Bob") = 209^158 mod 251 = 79 $
Hasil komputasi program membuktikan $K = K' = 79$ secara identik.

== Verifikasi ElGamal Teks 'HALO' Sesuai Slide Perkuliahan
Pengujian mencocokkan parameter enkripsi teks "HALO":
- Parameter Kunci: Prima $p = 2273$, generator $g = 3$, kunci privat penerima $x = 243$.
- Kunci Publik Penerima:
  $ y = 3^243 mod 2273 = 461 $
- Teks "HALO" dipetakan menjadi deret angka $07001114$, lalu dipartisi menjadi dua blok 4-digit: $m_1 = 700$ dan $m_2 = 1114$.
- Enkripsi Blok ($k_1 = 1463, k_2 = 2001$):
  - Blok 1: $a_1 = 3^1463 mod 2273 = 1439$, $b_1 = (461^1463 dot 700) mod 2273 = 74$. Diperoleh pasangan $c_1 = (1439, 74)$.
  - Blok 2: $a_2 = 3^2001 mod 2273 = 1220$, $b_2 = (461^2001 dot 1114) mod 2273 = 1682$. Diperoleh pasangan $c_2 = (1220, 1682)$.
- Dekripsi via Teorema Kecil Fermat ($p - 1 - x = 2273 - 1 - 243 = 2029$):
  - Blok 1: $a_1^(2029) = 1439^2029 mod 2273 = 1791$, $m_1 = (74 dot 1791) mod 2273 = 700$ ("0700" $->$ "HA").
  - Blok 2: $a_2^(2029) = 1220^2029 mod 2273 = 1125$, $m_2 = (1682 dot 1125) mod 2273 = 1114$ ("1114" $->$ "LO").
Teks pulih sempurna menjadi "HALO".

== Hasil Uji Otomatis Unit Test
Rangkaian pengujian unit test dijalankan melalui framework `pytest` pada lingkungan CachyOS (Python 3.14). Seluruh 12 skenario pengujian berstatus *PASSED*:

#align(center)[
#table(
  columns: (2.3fr, 3fr, 0.9fr),
  stroke: 0.5pt + luma(180),
  fill: (col, row) => if row == 0 { luma(240) } else { none },
  inset: 6.5pt,
  align: (left, left, center),
  [*Nama Test Case*], [*Fokus Pengujian*], [*Status*],
  [`test_is_prime`], [Uji batas bilangan bulat negatif, 0, 1, prima kecil, dan komposit], [PASSED],
  [`test_gcd_and_extended_gcd`], [Kebenaran pembagi terbesar dan relasi Bézout a*x + b*y = gcd(a, b)], [PASSED],
  [`test_mod_inverse`], [Eksistensi invers perkalian modular via Extended Euclidean], [PASSED],
  [`test_mod_pow`], [Akurasi eksponensiasi biner modular Square-and-Multiply], [PASSED],
  [`test_primitive_root_validation`], [Validasi generator sah g=3 vs non-generator g=2 modulo 7], [PASSED],
  [`test_find_primitive_root`], [Pencarian otomatis akar primitif terkecil sebuah bilangan prima], [PASSED],
  [`test_generate_prime`], [Pembangkitan bilangan prima acak dalam rentang nilai tertentu], [PASSED],
  [`test_dh_slide_example`], [Validasi kesesuaian numerik Diffie-Hellman contoh perkuliahan], [PASSED],
  [`test_dh_random_flow`], [Konsistensi derivasi kunci sesi bersama pada parameter acak], [PASSED],
  [`test_elgamal_slide_halo_example`], [Validasi kesesuaian numerik ElGamal teks 'HALO' contoh kuliah], [PASSED],
  [`test_elgamal_lecture_padding`], [Integritas penanganan padding 'X' pada teks ganjil 'LOGARITMA'], [PASSED],
  [`test_elgamal_utf8_mode`], [Enkripsi dan dekripsi teks umum UTF-8 dengan spasi dan simbol], [PASSED]
)
]

= Kesimpulan

Sistem kriptografi Diffie-Hellman dan ElGamal telah berhasil diimplementasikan secara mandiri dari dasar dengan memenuhi seluruh kriteria penugasan:
- Seluruh algoritma teori bilangan dibangun secara transparan pada modul `crypto_core.py` murni tanpa ketergantungan pada pustaka kriptografi eksternal.
- Komputasi aljabar modular program terbukti akurat dan identik terhadap contoh numerik perkuliahan pada slide pertemuan ke-9.
- Sistem mendukung skema perkuliahan (pemetaan desimal dua digit dengan pelepasan bantalan otomatis) serta skema biner standar industri (UTF-8).
- Antarmuka Streamlit menyediakan visualisasi transparan untuk setiap tahapan pertukaran kunci, proses enkripsi/dekripsi per blok, serta inspeksi keamanan terhadap penyadap pasif.
