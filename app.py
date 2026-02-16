import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="SILA Sovereign OS", page_icon="🛡️")
st.title("🛡️ SILA: SOVEREIGN OS")

try:
    # 1. Pastikan Kunci Terbaca
    kunci_api = st.secrets["GOOGLE_API_KEY"]
    
    # 2. PAKSA JALUR PRODUKSI (v1)
    # Kita buang 'rest' dan biarkan dia pakai default, tapi ganti cara panggilnya
    genai.configure(api_key=kunci_api)
    
    # 3. AKTIFKAN MODEL TANPA 'models/'
    # Terkadang library versi tertentu justru error jika pakai prefix
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    st.success("✅ DNA Stabil: Pangkalan Siap Operasional")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

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
    st.error(f"⚠️ Masalah Logistik: {e}")
