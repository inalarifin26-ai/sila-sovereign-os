import streamlit as st
import google.generativeai as genai

# --- DNA CONFIGURATION ---
st.set_page_config(page_title="SILA Sovereign OS", page_icon="🛡️")

# Injeksi Kunci API Langsung (Bypass Secrets)
genai.configure(api_key="AIzaSyCW86D0dmfGwliqF0oPHhGp6COXKy8Q3wI")

# Inisialisasi Model Absolut (Solusi Error 404)
# Menggunakan jalur lengkap 'models/' untuk memastikan sinkronisasi API
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

# --- USER INTERFACE ---
st.title("🛡️ SILA: SOVEREIGN OS")
st.markdown("---")
st.info("🛰️ **STATUS SYSTEM:** DNA ANCHOR ACTIVE")

# Memory State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render Chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- LOGIKA INSTRUKSI ---
if prompt := st.chat_input("Apa instruksi Anda, Chief?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Protokol Respon SILA
            response = model.generate_content(f"Jawablah sebagai SILA Sovereign OS yang taktis: {prompt}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"⚠️ SILA Terhambat: {e}")
