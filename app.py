import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="SILA Sovereign OS", page_icon="🛡️")
st.title("🛡️ SILA: SOVEREIGN OS")

try:
    # 1. Pastikan Logistik Kunci Aman
    kunci_api = st.secrets["GOOGLE_API_KEY"]
    
    # 2. PAKSA JALUR REST (Mencegah 404 v1beta)
    genai.configure(api_key=kunci_api, transport='rest')
    
    # 3. PAKAI MODEL PRO (Lebih Stabil daripada Flash di v1beta)
    model = genai.GenerativeModel('gemini-pro')
    
    st.success("✅ Sistem Mengenali DNA: Semua Oke")

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
            # Panggilan murni tanpa embel-embel tambahan
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

except Exception as e:
    st.error(f"⚠️ Gangguan Radar: {e}")
