import streamlit as st
import google.generativeai as genai

# --- 🛡️ CONFIG ---
st.set_page_config(page_title="SILA Sovereign OS", page_icon="🛡️")
st.title("🛡️ SILA: SOVEREIGN OS")

try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    
    # Inisialisasi Model Tanpa Embel-embel
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction="Anda SILA, partner casual Chief. Bicara santai tapi sopan."
    )
    
    # Indikator Sukses
    model_list = [m.name for m in genai.list_models()]
    st.success(f"✅ DNA Anchor Terkunci: {len(model_list)} Model Oke")

    # --- 💬 CHAT LOGIC ---
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ada misi apa hari ini, Chief?"):
        # 1. Simpan chat user
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        # 2. Ambil jawaban assistant
        with st.chat_message("assistant"):
            # Pakai start_chat yang paling stabil
            chat = model.start_chat(history=[])
            response = chat.send_message(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

except Exception as e:
    st.error(f"⚠️ Gangguan: {e}")
