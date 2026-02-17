import streamlit as st
import google.generativeai as genai

# 1. SET API (Hanya Fungsi Koneksi)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # Gunakan model paling dasar untuk tes
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.write("Sila: API Key Belum Ada.")
    st.stop()

# 2. TES KONEKSI LANGSUNG
st.title("SILA Connectivity Test")
if st.button("PING AI STUDIO"):
    try:
        # Tes kirim sinyal paling simpel
        response = model.generate_content("Ping!")
        st.success(f"KONEKSI TEMBUS: {response.text}")
    except Exception as e:
        st.error(f"KONEKSI GAGAL: {e}")
