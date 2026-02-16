import streamlit as st
import google.generativeai as genai

# --- 🛡️ CONFIG PANGKALAN ---
st.set_page_config(page_title="SILA Sovereign OS", page_icon="🛡️")
st.title("🛡️ SILA: SOVEREIGN OS")

try:
    # 1. Definisi Kunci (Cegah NameError)
    kunci_api = st.secrets["GOOGLE_API_KEY"]
    
    # 2. Konfigurasi Sistem
    genai.configure(api_key=kunci_api)
    
    # 3. Inisialisasi Model Jalur Lengkap (Bypass 404)
    # Menggunakan 'models/' di depan untuk paksa jalur stabil
    model = genai.GenerativeModel(
        model_name='models/gemini-1.5-flash',
        system_instruction="Anda adalah SILA, partner setia Chief. Bicara casual, akrab, dan solutif."
    )
    
    # Indikator Sukses
    st.success("✅ Sistem Mengenali DNA: Semua Oke")

    # --- 💬 LOGIKA KOMUNIKASI ---
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Tampilkan riwayat chat
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # 4. KOLOM INPUT (The Mission Control)
    if prompt := st.chat_input("Ada misi apa hari ini, Chief?"):
        # Simpan & Tampilkan input user
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        # Proses Respon SILA
        with st.chat_message("assistant"):
            # Panggil konten tanpa embel-embel api_version yang bikin error
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

except Exception as e:
    # Jika masih ada error, tampilkan dengan jelas di layar
    st.error(f"⚠️ Gangguan Radar: {e}")
