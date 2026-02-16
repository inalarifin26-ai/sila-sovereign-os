import streamlit as st
import google.generativeai as genai

# --- 🛡️ CONFIG PANGKALAN ---
st.set_page_config(page_title="SILA Sovereign OS", page_icon="🛡️")
st.title("🛡️ SILA: SOVEREIGN OS")

try:
    # 1. Pastikan Kunci Terbaca
    kunci_api = st.secrets["GOOGLE_API_KEY"]
    
    # 2. KONFIGURASI PAKSA JALUR PRODUKSI
    # Kita buang instruksi transport='rest' sementara dan pakai default v1
    genai.configure(api_key=kunci_api)
    
    # 3. AKTIFKAN MODEL TANPA EMBEL-EMBEL
    # Menggunakan Gemini 1.5 Flash karena ini model terbaru yang paling didukung
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    st.success("✅ DNA Stabil: Pangkalan Siap Operasional")

    # --- 💬 LOGIKA KOMUNIKASI ---
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # 4. KOLOM INPUT
    if prompt := st.chat_input("Sapa SILA di sini, Chief..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            # PROSES PENYALURAN PESAN
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

except Exception as e:
    # Laporan jika radar masih mendeteksi 404
    st.error(f"⚠️ Masalah Logistik: {e}")
