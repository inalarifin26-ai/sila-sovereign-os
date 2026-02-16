import streamlit as st
import requests

st.set_page_config(page_title="SILA Sovereign OS", page_icon="🛡️")
st.title("🛡️ SILA: SOVEREIGN OS")

try:
    # 1. Ambil Kunci
    api_key = st.secrets["GOOGLE_API_KEY"]
    
    # 2. ALAMAT PUSAT (Paksa Jalur v1 - Bukan v1beta)
    # Ini adalah bypass total untuk menghidari error 404
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    st.success("✅ Jalur Darurat Aktif: DNA Stabil")

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
            # Request manual tanpa library genai
            payload = {"contents": [{"parts": [{"text": prompt}]}]}
            headers = {'Content-Type': 'application/json'}
            
            response = requests.post(url, json=payload, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                answer = result['candidates'][0]['content']['parts'][0]['text']
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                # Jika masih 404, kita akan lihat detailnya di sini
                st.error(f"⚠️ Gangguan Radar: {response.status_code} - {response.text}")

except Exception as e:
    st.error(f"⚠️ Masalah Logistik: {e}")
