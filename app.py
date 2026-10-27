"""
app.py
Antarmuka Interaktif Diffie-Hellman & ElGamal
Tugas 4 Kriptografi (A) - Kelompok 17
"""

import random
import streamlit as st
import crypto_core
import diffie_hellman
import elgamal

st.set_page_config(
    page_title="Diffie-Hellman & ElGamal Cryptosystem",
    page_icon="🔐",
    layout="wide",
)

SAMPLE_LECTURE_WORDS = [
    "HALO",
    "KRIPTOGRAFI",
    "LOGARITMA",
    "KOMPUTASI",
    "MATEMATIKA",
    "KEAMANAN",
    "MERDEKA",
]

SAMPLE_UTF8_TEXTS = [
    "Aku suka kriptografi.",
    "Diffie-Hellman",
    "ElGamal",
    "Kriptografi Kunci Publik 2026",
    "Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit...",
    (
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod "
        "tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, "
        "quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."
    ),
]

# ----------------------------------------------------------------------------
# Inisialisasi State Awal
# ----------------------------------------------------------------------------
initial_values = {
    "dh_n": 251,
    "dh_g": 6,
    "dh_x": 124,
    "dh_y": 158,
    "dh_result": None,
    "eg_p": 2273,
    "eg_g": 3,
    "eg_x": 243,
    "eg_mode": "Mode Materi Kuliah (A=00..Z=25)",
    "eg_plaintext": "HALO",
    "eg_custom_k": "1463, 2001",
    "eg_enc_records": None,
    "eg_dec_records": None,
    "eg_recovered_text": "",
    "eg_block_digits": 4,
    "eg_pad_count": 0,
    "eg_chunk_size": 1,
}

for key, val in initial_values.items():
    if key not in st.session_state:
        st.session_state[key] = val


# ----------------------------------------------------------------------------
# Callback Functions (Manajemen State)
# ----------------------------------------------------------------------------
def cb_preset_dh():
    st.session_state.dh_n = 251
    st.session_state.dh_g = 6
    st.session_state.dh_x = 124
    st.session_state.dh_y = 158
    st.session_state.dh_result = None


def cb_random_dh():
    params = diffie_hellman.generate_dh_parameters(200, 2000)
    st.session_state.dh_n = params["n"]
    st.session_state.dh_g = params["g"]
    st.session_state.dh_x = diffie_hellman.generate_dh_private_key(params["n"])
    st.session_state.dh_y = diffie_hellman.generate_dh_private_key(params["n"])
    st.session_state.dh_result = None


def cb_preset_elgamal():
    st.session_state.eg_p = 2273
    st.session_state.eg_g = 3
    st.session_state.eg_x = 243
    st.session_state.eg_mode = "Mode Materi Kuliah (A=00..Z=25)"
    st.session_state.eg_plaintext = "HALO"
    st.session_state.eg_custom_k = "1463, 2001"
    st.session_state.eg_enc_records = None
    st.session_state.eg_dec_records = None
    st.session_state.eg_recovered_text = ""
    st.session_state.eg_pad_count = 0


def cb_random_elgamal():
    new_p = crypto_core.generate_prime(1000, 4000)
    new_g = crypto_core.find_primitive_root(new_p)
    new_x = diffie_hellman.generate_dh_private_key(new_p)
    st.session_state.eg_p = new_p
    st.session_state.eg_g = new_g
    st.session_state.eg_x = new_x

    if st.session_state.eg_mode == "Mode Materi Kuliah (A=00..Z=25)":
        st.session_state.eg_plaintext = random.choice(SAMPLE_LECTURE_WORDS)
    else:
        st.session_state.eg_plaintext = random.choice(SAMPLE_UTF8_TEXTS)

    st.session_state.eg_custom_k = ""
    st.session_state.eg_enc_records = None
    st.session_state.eg_dec_records = None
    st.session_state.eg_recovered_text = ""
    st.session_state.eg_pad_count = 0


def cb_mode_change():
    """Membersihkan hasil enkripsi lama saat berganti mode."""
    st.session_state.eg_enc_records = None
    st.session_state.eg_dec_records = None
    st.session_state.eg_recovered_text = ""
    st.session_state.eg_pad_count = 0


# ----------------------------------------------------------------------------
# Header Aplikasi
# ----------------------------------------------------------------------------
st.title("Sistem Kriptografi Diffie-Hellman & ElGamal")
st.caption(
    "Implementasi mandiri berbasis Logaritma Diskrit tanpa pustaka kriptografi pihak ketiga | Kelompok 17"
)

tab_dh, tab_eg, tab_lab = st.tabs([
    "🤝 Pertukaran Kunci Diffie-Hellman",
    "✉️ Kriptosistem ElGamal",
    "🔬 Lab Teori & Logaritma Diskrit",
])

# ============================================================================
# TAB 1: DIFFIE-HELLMAN KEY EXCHANGE
# ============================================================================
with tab_dh:
    st.subheader("Protokol Pertukaran Kunci Diffie-Hellman")
    st.markdown(
        "Membangkitkan kunci sesi simetris bersama ($K = K'$) melalui saluran komunikasi publik yang tidak aman."
    )

    c1, c2, _ = st.columns([1.2, 1.2, 2])
    c1.button(
        "Preset Materi Kuliah (n=251, g=6)",
        on_click=cb_preset_dh,
        width="stretch",
    )
    c2.button(
        "Acak Parameter Baru",
        on_click=cb_random_dh,
        width="stretch",
    )

    col_param1, col_param2 = st.columns(2)
    with col_param1:
        n_val = st.number_input(
            "Bilangan Prima Modulus (n)",
            min_value=5,
            step=1,
            key="dh_n",
        )
    with col_param2:
        g_val = st.number_input(
            "Akar Primitif / Generator (g)",
            min_value=2,
            step=1,
            key="dh_g",
        )

    is_valid_dh, msg_dh = diffie_hellman.validate_dh_parameters(
        int(n_val), int(g_val), param_name="n"
    )

    if not is_valid_dh:
        st.error(f"Parameter Tidak Valid: {msg_dh}")
    else:
        st.success(f"Parameter Publik Sah: {msg_dh} (panjang siklus = {n_val - 1})")

        col_alice, col_bob = st.columns(2)
        with col_alice:
            with st.container(border=True):
                st.markdown("#### Sisi Alice")
                x_val = st.number_input(
                    f"Kunci Privat Alice (x), rentang 1 < x < {n_val - 1}",
                    min_value=2,
                    max_value=max(2, int(n_val) - 2),
                    step=1,
                    key="dh_x",
                )
                X_pub = diffie_hellman.compute_dh_public_key(
                    int(g_val), int(x_val), int(n_val)
                )
                st.latex(f"X = g^x \\bmod n = {g_val}^{{{x_val}}} \\bmod {n_val} = {X_pub}")
                st.info(f"Kunci Publik Alice dikirim ke Bob: **X = {X_pub}**")

        with col_bob:
            with st.container(border=True):
                st.markdown("#### Sisi Bob")
                y_val = st.number_input(
                    f"Kunci Privat Bob (y), rentang 1 < y < {n_val - 1}",
                    min_value=2,
                    max_value=max(2, int(n_val) - 2),
                    step=1,
                    key="dh_y",
                )
                Y_pub = diffie_hellman.compute_dh_public_key(
                    int(g_val), int(y_val), int(n_val)
                )
                st.latex(f"Y = g^y \\bmod n = {g_val}^{{{y_val}}} \\bmod {n_val} = {Y_pub}")
                st.info(f"Kunci Publik Bob dikirim ke Alice: **Y = {Y_pub}**")

        if st.button("Hitung Kunci Sesi Bersama", type="primary", width="stretch"):
            K_alice = diffie_hellman.compute_dh_shared_secret(
                Y_pub, int(x_val), int(n_val)
            )
            K_bob = diffie_hellman.compute_dh_shared_secret(
                X_pub, int(y_val), int(n_val)
            )
            st.session_state.dh_result = {
                "K_alice": K_alice,
                "K_bob": K_bob,
                "X": X_pub,
                "Y": Y_pub,
                "x": int(x_val),
                "y": int(y_val),
                "n": int(n_val),
                "g": int(g_val),
            }

        res_dh = st.session_state.dh_result
        if res_dh:
            st.divider()
            c_res1, c_res2 = st.columns(2)
            with c_res1:
                st.markdown("**Perhitungan Kunci Sesi oleh Alice:**")
                st.latex(
                    f"K = Y^x \\bmod n = {res_dh['Y']}^{{{res_dh['x']}}} \\bmod {res_dh['n']} = {res_dh['K_alice']}"
                )
            with c_res2:
                st.markdown("**Perhitungan Kunci Sesi oleh Bob:**")
                st.latex(
                    f"K' = X^y \\bmod n = {res_dh['X']}^{{{res_dh['y']}}} \\bmod {res_dh['n']} = {res_dh['K_bob']}"
                )

            if res_dh["K_alice"] == res_dh["K_bob"]:
                st.success(
                    f"Kunci Sesi Berhasil Disepakati: **K = K' = {res_dh['K_alice']}**"
                )

            with st.expander("Inspeksi Keamanan: Sudut Pandang Penyadapan (Eve)"):
                st.markdown(
                    "Penyadap di saluran transmisi publik hanya melihat parameter berikut:"
                )
                st.code(
                    f"Parameter Terbuka: n = {res_dh['n']}, g = {res_dh['g']}\n"
                    f"Nilai Transmisi Terbuka: X = {res_dh['X']}, Y = {res_dh['Y']}",
                    language="text",
                )
                st.markdown(
                    "Untuk menemukan nilai kunci sesi $K$, pihak ketiga harus menyelesaikan persoalan "
                    "logaritma diskrit ($X \\equiv g^x \\pmod n$) guna memulihkan nilai $x$ atau $y$."
                )

# ============================================================================
# TAB 2: KRIPTOSISTEM ELGAMAL
# ============================================================================
with tab_eg:
    st.subheader("Kriptosistem Kunci Publik ElGamal")
    st.markdown(
        "Mendukung pembentukan kunci publik-privat, enkripsi per blok ke pasangan $(a, b)$, dan dekripsi invers modular."
    )

    c_eg1, c_eg2, _ = st.columns([1.2, 1.2, 2])
    c_eg1.button(
        "Preset Materi Kuliah ('HALO')",
        on_click=cb_preset_elgamal,
        width="stretch",
    )
    c_eg2.button(
        "Acak Parameter ElGamal",
        on_click=cb_random_elgamal,
        width="stretch",
    )

    col_eg1, col_eg2, col_eg3 = st.columns(3)
    with col_eg1:
        eg_p_val = st.number_input(
            "Bilangan Prima (p)",
            min_value=5,
            step=1,
            key="eg_p",
        )
    with col_eg2:
        eg_g_val = st.number_input(
            "Akar Primitif (g)",
            min_value=2,
            step=1,
            key="eg_g",
        )
    with col_eg3:
        eg_x_val = st.number_input(
            f"Kunci Privat Penerima (x), rentang 1 < x < {eg_p_val - 1}",
            min_value=2,
            max_value=max(2, int(eg_p_val) - 2),
            step=1,
            key="eg_x",
        )

    is_valid_eg, msg_eg = diffie_hellman.validate_dh_parameters(
        int(eg_p_val), int(eg_g_val), param_name="p"
    )

    if not is_valid_eg:
        st.error(f"Parameter Tidak Valid: {msg_eg}")
    else:
        try:
            keypair = elgamal.generate_elgamal_keypair(
                int(eg_p_val), int(eg_g_val), preferred_x=int(eg_x_val)
            )
            st.success(
                f"Pasangan Kunci Terbentuk: Kunci Publik **(y={keypair['y']}, g={keypair['g']}, p={keypair['p']})** | "
                f"Kunci Privat **x={keypair['x']}**"
            )
        except Exception as err:
            st.error(f"Gagal membentuk pasangan kunci: {err}")
            keypair = None

        st.divider()
        mode_val = st.radio(
            "Pilih Skema Pengodean Pesan",
            ["Mode Materi Kuliah (A=00..Z=25)", "Mode Teks Umum (UTF-8)"],
            horizontal=True,
            key="eg_mode",
            on_change=cb_mode_change,
        )

        if mode_val == "Mode Materi Kuliah (A=00..Z=25)":
            st.info(
                "ℹ️ **Ketentuan Mode Materi Kuliah**: Sesuai modul perkuliahan (halaman 16), mode ini memetakan "
                "26 alfabet ($A=00 \\dots Z=25$). Karakter non-alfabet (spasi, angka, tanda baca) diabaikan dan huruf kecil "
                "otomatis dikapitalisasi. Jika panjang huruf ganjil, huruf pengganjal ('X') ditambahkan pada blok akhir agar pas 4 digit desimal."
            )
        else:
            st.info(
                "🌐 **Ketentuan Mode Teks Umum (UTF-8)**: Pesan dipartisi secara biner (byte chunking Big-Endian). "
                "Mendukung penuh spasi, huruf besar/kecil, tanda baca, simbol, dan kalimat panjang."
            )

        plaintext_val = st.text_input(
            "Teks Plaintext yang dikirim",
            key="eg_plaintext",
        )

        st.text_input(
            "Nilai k Acak per Blok (pisahkan koma, kosongkan untuk acak otomatis)",
            key="eg_custom_k",
            help="Contoh: 1463, 2001 untuk mencocokkan contoh slide materi kuliah.",
        )

        if st.button("Enkripsi Pesan", type="primary"):
            if not keypair:
                st.warning("Perbaiki parameter kunci sebelum mengenkripsi pesan.")
            else:
                try:
                    custom_k_str = st.session_state.eg_custom_k.strip()
                    k_list = None
                    if custom_k_str:
                        k_list = [
                            int(k.strip())
                            for k in custom_k_str.split(",")
                            if k.strip()
                        ]

                    if mode_val == "Mode Materi Kuliah (A=00..Z=25)":
                        blocks, block_digits, num_str, pad_count = elgamal.text_to_lecture_blocks(
                            plaintext_val, keypair["p"]
                        )
                        st.session_state.eg_block_digits = block_digits
                        st.session_state.eg_pad_count = pad_count

                        enc_records = elgamal.encrypt_elgamal_blocks(
                            blocks,
                            keypair["y"],
                            keypair["g"],
                            keypair["p"],
                            custom_k_list=k_list,
                        )
                    else:
                        blocks, chunk_size = elgamal.text_to_utf8_blocks(
                            plaintext_val, keypair["p"]
                        )
                        st.session_state.eg_chunk_size = chunk_size
                        st.session_state.eg_pad_count = 0
                        enc_records = elgamal.encrypt_elgamal_blocks(
                            blocks,
                            keypair["y"],
                            keypair["g"],
                            keypair["p"],
                            custom_k_list=k_list,
                        )

                    st.session_state.eg_enc_records = enc_records
                    st.session_state.eg_dec_records = None
                    st.session_state.eg_recovered_text = ""
                except Exception as err:
                    st.error(f"Gagal mengenkripsi pesan: {err}")

        enc_res = st.session_state.eg_enc_records
        if enc_res:
            st.markdown(f"#### Hasil Enkripsi: {len(enc_res)} Blok Ciphertext $(a, b)$")
            table_enc = [
                {
                    "Blok": r["block_index"],
                    "Plaintext Integer (m)": str(r["m"]),
                    "Nilai Acak (k)": str(r["k"]),
                    "a = g^k mod p": str(r["a"]),
                    "b = (y^k * m) mod p": str(r["b"]),
                    "Ciphertext Pair (a, b)": f"({r['a']}, {r['b']})",
                }
                for r in enc_res
            ]
            st.dataframe(table_enc, width="stretch", hide_index=True)

            if st.button("Dekripsi Ciphertext", type="primary"):
                try:
                    cipher_pairs = [(r["a"], r["b"]) for r in enc_res]
                    dec_records = elgamal.decrypt_elgamal_blocks(
                        cipher_pairs, keypair["x"], keypair["p"]
                    )
                    st.session_state.eg_dec_records = dec_records

                    if mode_val == "Mode Materi Kuliah (A=00..Z=25)":
                        recovered = elgamal.lecture_blocks_to_text(
                            [d["m"] for d in dec_records],
                            st.session_state.eg_block_digits,
                            pad_count=st.session_state.eg_pad_count,
                        )
                    else:
                        recovered = elgamal.utf8_blocks_to_text(
                            [d["m"] for d in dec_records],
                            st.session_state.eg_chunk_size,
                        )
                    st.session_state.eg_recovered_text = recovered
                except Exception as err:
                    st.error(f"Gagal mendekripsi ciphertext: {err}")

        dec_res = st.session_state.eg_dec_records
        if dec_res:
            st.markdown("#### Hasil Dekripsi & Pemulihan Plaintext")
            table_dec = [
                {
                    "Blok": r["block_index"],
                    "Ciphertext a": str(r["a"]),
                    "Ciphertext b": str(r["b"]),
                    "a^(p-1-x) mod p": str(r["ax_inv"]),
                    "m = b * a^(p-1-x) mod p": str(r["m"]),
                }
                for r in dec_res
            ]
            st.dataframe(table_dec, width="stretch", hide_index=True)
            st.success(
                f"Plaintext Pulih Sepenuhnya: **{st.session_state.eg_recovered_text}**"
            )
            if mode_val == "Mode Materi Kuliah (A=00..Z=25)" and st.session_state.eg_pad_count > 0:
                st.caption(
                    f"Catatan: {st.session_state.eg_pad_count} huruf padding 'X' pada blok terakhir telah dilepas otomatis untuk memulihkan teks asli."
                )

# ============================================================================
# TAB 3: LAB TEORI & LOGARITMA DISKRIT
# ============================================================================
with tab_lab:
    st.subheader("Laboratorium Teori: Akar Primitif & Logaritma Diskrit")
    st.markdown(
        "Verifikasi langsung panjang siklus generator modulo $p$ dan simulasi pencarian logaritma diskrit."
    )

    col_lab1, col_lab2 = st.columns(2)
    with col_lab1:
        with st.container(border=True):
            st.markdown("#### Uji Siklus Akar Primitif")
            st.caption("Memverifikasi apakah $g$ menghasilkan $p-1$ elemen unik.")
            lp = st.number_input(
                "Nilai Prima (p)", min_value=3, value=7, step=1, key="in_lp"
            )
            lg = st.number_input(
                "Basis Generator (g)", min_value=2, value=3, step=1, key="in_lg"
            )

            if st.button("Hitung Siklus Pangkat", width="stretch"):
                is_prim = crypto_core.is_primitive_root(int(lg), int(lp))
                cycle_data = []
                seen = set()
                has_duplicate = False

                for power in range(1, int(lp)):
                    val = crypto_core.mod_pow(int(lg), power, int(lp))
                    is_dup = val in seen
                    if is_dup:
                        has_duplicate = True
                    seen.add(val)
                    cycle_data.append({
                        "Pangkat (i)": f"{lg}^{power} mod {lp}",
                        "Nilai": val,
                        "Status": "Duplikat" if is_dup else "Unik",
                    })

                st.dataframe(cycle_data, width="stretch", hide_index=True)
                if is_prim:
                    st.success(
                        f"g={lg} adalah akar primitif dari p={lp}. Panjang siklus mencapai nilai maksimum p - 1 = {lp - 1}."
                    )
                else:
                    st.warning(
                        f"g={lg} BUKAN akar primitif dari p={lp}. Nilai berulang sebelum mencapai panjang siklus {lp - 1}."
                    )

    with col_lab2:
        with st.container(border=True):
            st.markdown("#### Eksplorasi Persoalan Logaritma Diskrit (DLP)")
            st.caption("Mencari nilai $x$ pada kongruensi: $b \\equiv g^x \\pmod p$.")
            dlp_p = st.number_input(
                "Modulus Prima (p)", min_value=3, value=41, step=1, key="in_dlp_p"
            )
            dlp_g = st.number_input(
                "Basis Akar Primitif (g)", min_value=2, value=7, step=1, key="in_dlp_g"
            )
            dlp_b = st.number_input(
                "Nilai Kongruen (b)", min_value=1, value=15, step=1, key="in_dlp_b"
            )

            if st.button("Cari Nilai x (Brute-Force Search)", width="stretch"):
                found_x = None
                steps = []
                for candidate in range(int(dlp_p)):
                    cur = crypto_core.mod_pow(int(dlp_g), candidate, int(dlp_p))
                    if cur == int(dlp_b):
                        found_x = candidate
                        steps.append({
                            "x": candidate,
                            f"g^x mod {dlp_p}": cur,
                            "Status": "Cocok",
                        })
                        break
                    else:
                        if len(steps) < 8:
                            steps.append({
                                "x": candidate,
                                f"g^x mod {dlp_p}": cur,
                                "Status": "Salah",
                            })

                if found_x is not None:
                    st.success(f"Ditemukan logaritma diskrit: **x = {found_x}**")
                    st.latex(f"{dlp_g}^{{{found_x}}} \\equiv {dlp_b} \\pmod{{{dlp_p}}}")
                else:
                    st.error("Nilai x tidak ditemukan dalam rentang modulus.")

                if steps:
                    st.caption("Langkah penelusuran (pencarian linier):")
                    st.dataframe(steps, width="stretch", hide_index=True)
