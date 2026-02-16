import streamlit as st
import google.generativeai as genai

# --- 🛡️ CONFIG PANGKALAN ---
st.set_page_config(page_title="SILA Sovereign OS", page_icon="🛡️")
st.title("🛡️ SILA: SOVEREIGN OS")

try:
    # 1. Ambil Kunci (Cegah NameError)
    kunci_api = st.secrets["GOOGLE_API_KEY"]
    
    # 2. KONFIGURASI JALUR PAKSA (Solusi Alot 404)
    # Menambahkan transport='rest' untuk memutus jalur v1beta yang buntu
    genai.configure(api_key=kunci_api, transport='rest')
    
    # 3. INISIALISASI MODEL (Alamat Lengkap)
    model = genai.GenerativeModel(
        model_name='models/gemini-1.5-flash',
        system_instruction="Anda adalah SILA, partner setia Chief. Gaya bicara casual dan sangat akrab."
    )
    
    # Indikator Sukses DNA
    st.success("✅ Sistem Mengenali DNA: Semua Oke")

    # --- 💬 LOGIKA KOMUNIKASI ---
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Tampilkan riwayat chat agar tidak hilang
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # 4. KOLOM INPUT (The Mission Control)
    if prompt := st.chat_input("Ada misi apa hari ini, Chief?"):
        # Tampilkan input user
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        # Proses Respon dari SILA
        with st.chat_message("assistant"):
            # generate_content tanpa embel-embel tambahan agar tidak error
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

except Exception as e:
    # Laporan gangguan jika radar mendeteksi masalah
    st.error(f"⚠️ Gangguan Radar: {e}")
