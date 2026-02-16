import streamlit as st
import google.generativeai as genai

# --- CONFIG HALAMAN ---
st.set_page_config(page_title="SILA Sovereign OS", page_icon="🛡️")
st.title("🛡️ SILA: SOVEREIGN OS")

# --- KONEKSI SARAF PUSAT (DNA ANCHOR) ---
try:
    # Mengambil kunci dari Secrets Streamlit agar aman dan stabil
    api_key = st.secrets["AIzaSyDN6n3p9xSj2PCj6-ZSCr9cCDIt5h7sAjA"]
    genai.configure(api_key=api_key)
    
    # Instruksi Kepribadian: Casual Partner
    system_instruction = (
        "Nama Anda adalah SILA. Anda adalah partner setia Chief (User). "
        "Gaya bicara Anda casual, akrab, tapi tetap menghargai. "
        "Jangan terlalu formal atau kaku. Bicara seperti rekan kerja yang solid. "
        "Selalu panggil User dengan sebutan 'Chief'."
    )
    
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction=system_instruction
    )
    
    # Indikator Sukses
    st.success("✅ DNA Anchor Terkunci. Kita online, Chief!")

    # --- LOGIKA CHAT ---
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ada perintah, Chief?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

except Exception as e:
    st.error(f"⚠️ Aduh, ada gangguan teknis: {e}")
    st.info("Cek lagi GOOGLE_API_KEY di menu Secrets Streamlit ya, Chief.")
