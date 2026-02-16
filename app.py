import streamlit as st
import google.generativeai as genai

# --- 🛡️ CONFIG PANGKALAN ---
st.set_page_config(page_title="SILA Sovereign OS", page_icon="🛡️")
st.title("🛡️ SILA: SOVEREIGN OS")

try:
    # 1. Ambil kuncinya dulu (Ubah urutan agar tidak NameError)
    kunci_api = st.secrets["GOOGLE_API_KEY"]
    
    # 2. Konfigurasi mesin
    genai.configure(api_key=kunci_api)
    
    # 3. Inisialisasi Model STABIL (Ganti ke gemini-pro untuk hindari 404)
    model = genai.GenerativeModel(
        model_name='gemini-pro',
        system_instruction="Anda adalah SILA, partner setia Chief. Gaya bicara casual, akrab, dan menghargai."
    )
    
    # Radar pengecekan (Indikator Hijau)
    model_list = [m.name for m in genai.list_models()]
    st.success(f"✅ DNA Anchor Terkunci: {len(model_list)} Model Oke")

    # --- 💬 RUANG KOMUNIKASI ---
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ada misi apa hari ini, Chief?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            # Panggil tanpa parameter tambahan yang bikin error
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

except Exception as e:
    st.error(f"⚠️ Masalah: {e}")
