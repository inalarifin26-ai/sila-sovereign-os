import streamlit as st
import google.generativeai as genai

# 1. Judul & Konfigurasi Dasar
st.set_page_config(page_title="SILA Sovereign OS", page_icon="🛡️")
st.title("🛡️ SILA: SOVEREIGN OS")

try:
    # 2. Inisialisasi Keamanan
    kunci = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=kunci)
    model = genai.GenerativeModel('gemini-pro')
    
    # Indikator Sukses yang sudah muncul tadi
    st.success("✅ Sistem Mengenali DNA: Semua Oke")

    # 3. MEMORY SYSTEM (Agar chat tidak hilang saat dikirim)
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Tampilkan riwayat chat jika ada
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # 4. PASANG KOLOM CHAT (Ini yang tadi hilang)
    if prompt := st.chat_input("Ada misi apa hari ini, Chief?"):
        # Tampilkan chat user
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        # Respon dari SILA
        with st.chat_message("assistant"):
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

except Exception as e:
    st.error(f"⚠️ Masalah Teknis: {e}")
