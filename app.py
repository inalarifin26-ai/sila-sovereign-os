import streamlit as st
import google.generativeai as genai

# --- 🛡️ CONFIG PANGKALAN ---
st.set_page_config(page_title="SILA Sovereign OS", page_icon="🛡️")
st.title("🛡️ SILA: SOVEREIGN OS")

try:
    # 1. DEFINISIKAN dulu variabelnya agar tidak NameError
    kunci_api = st.secrets["GOOGLE_API_KEY"]
    
    # 2. KONFIGURASI sistem menggunakan variabel tersebut
    genai.configure(api_key=kunci_api)
    
    # 3. INISIALISASI Model
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction="Anda SILA, partner setia Chief. Bicara casual dan akrab."
    )
    
    # Radar pengecekan sukses
    model_list = [m.name for m in genai.list_models()]
    st.success(f"✅ DNA Anchor Terkunci: {len(model_list)} Model Oke")

    # --- 💬 RUANG CHAT ---
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ada perintah, Chief?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

except Exception as e:
    st.error(f"⚠️ Aduh Chief, sistem bilang: {e}")
