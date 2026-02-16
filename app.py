import streamlit as st
import google.generativeai as genai

# Konfigurasi Kunci
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

st.set_page_config(page_title="SILA: SOVEREIGN OS")
st.title("🛡️ SILA: SOVEREIGN OS")
st.write("Status: DNA ANCHOR ACTIVE")

# Inisialisasi Model Stabil
model = genai.GenerativeModel('gemini-1.5-flash')

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Perintah Anda, Chief?"):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    # Respon SILA
    response = model.generate_content(f"Kamu adalah SILA Sovereign OS. Bantu Chief: {prompt}")
    with st.chat_message("assistant"):
        st.write(response.text)
    st.session_state.chat_history.append({"role": "assistant", "content": response.text})
