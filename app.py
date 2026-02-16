import streamlit as st
import google.generativeai as genai

# --- 1. SETTING DASAR ---
st.set_page_config(page_title="SILA Sovereign OS", page_icon="🛡️")

# Injeksi Kunci API (Pastikan tidak ada spasi tambahan)
genai.configure(api_key="AIzaSyCW86D0dmfGwliqF0oPHhGp6COXKy8Q3wI")

# --- 2. KUNCI JALUR (Agar Bisa 'Join') ---
# Kita menggunakan 'models/gemini-1.5-flash' agar server tidak tersesat ke jalur beta
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

# --- 3. ANTARMUKA (UI) ---
st.title("🛡️ SILA: SOVEREIGN OS")
st.markdown("---")
st.info("🛰️ **STATUS SYSTEM:** DNA ANCHOR ACTIVE")

# Inisialisasi Memori Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan riwayat pesan
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. LOGIKA CHAT ---
if prompt := st.chat_input("Instruksi Anda, Chief?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Mengirim instruksi ke otak Gemini 1.5 Flash
            response = model.generate_content(f"Jawablah sebagai SILA OS: {prompt}")
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            # Jika 'Join' gagal, sistem akan memberi tahu detailnya
            st.error(f"⚠️ Jalur Terputus: {e}")
