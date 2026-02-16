import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="SILA Sovereign OS", page_icon="🛡️")
st.title("🛡️ SILA: SOVEREIGN OS")

try:
    # 1. Pastikan Kunci Terbaca
    kunci = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=kunci, transport='rest') # Paksa jalur stabil
    
    # 2. Pakai Pro agar tidak ada drama 404 Flash
    model = genai.GenerativeModel('gemini-pro')
    
    st.success("✅ DNA Stabil: Pangkalan Siap Operasional")
    
    if prompt := st.chat_input("Sapa SILA di sini, Chief..."):
        with st.chat_message("user"):
            st.write(prompt)
        with st.chat_message("assistant"):
            response = model.generate_content(prompt)
            st.write(response.text)

except Exception as e:
    st.error(f"⚠️ Masalah Logistik: {e}")
