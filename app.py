import streamlit as st
import google.generativeai as genai
from google.generativeai.types import RequestOptions # Tambahan untuk paksa jalur

st.set_page_config(page_title="SILA Sovereign OS", page_icon="🛡️")
st.title("🛡️ SILA: SOVEREIGN OS")

try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    
    # KUNCI UTAMA: Kita paksa lewat 'v1' di setiap pengiriman pesan
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Radar Pengecekan
    model_list = [m.name for m in genai.list_models()]
    st.success(f"✅ DNA Anchor Terkunci: {len(model_list)} Model Oke")

    if prompt := st.chat_input("Ada misi apa hari ini, Chief?"):
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            # Paksa request menggunakan jalur v1 secara eksplisit
            response = model.generate_content(
                prompt,
                request_options=RequestOptions(api_version='v1')
            )
            st.markdown(response.text)
            
except Exception as e:
    st.error(f"⚠️ Masalah: {e}")
