import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="SILA Sovereign OS", page_icon="🛡️")

try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    
    # Gunakan inisialisasi paling bersih
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Indikator Sukses
    model_list = [m.name for m in genai.list_models()]
    st.success(f"✅ DNA Anchor Terkunci: {len(model_list)} Model Oke")

    if prompt := st.chat_input("Ada misi apa hari ini, Chief?"):
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            # Langsung panggil tanpa tambahan yang bikin error
            response = model.generate_content(prompt)
            st.markdown(response.text)

except Exception as e:
    st.error(f"⚠️ Masalah: {e}")
