import streamlit as st
import google.generativeai as genai

# --- KONEKSI KE SECRETS ---
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except:
    st.error("DNA Anchor Error: Cek Secrets Anda!")
    st.stop()

# --- SETUP MODEL ---
model = genai.GenerativeModel('gemini-1.5-flash')

# --- UI SILA ---
st.title("🛡️ SILA: SOVEREIGN OS")
st.write("Status: DNA ANCHOR ACTIVE")

if prompt := st.chat_input("Perintah Anda, Chief?"):
    with st.chat_message("user"):
        st.write(prompt)

    # Respon AI
    response = model.generate_content(f"Analisis sebagai SILA: {prompt}")
    with st.chat_message("assistant"):
        st.write(response.text)
