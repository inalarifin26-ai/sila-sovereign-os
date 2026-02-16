import streamlit as st
import google.generativeai as genai

# --- 1. KONFIGURASI SESUAI SARAN SILA ---
st.set_page_config(page_title="SILA Sovereign OS", page_icon="🛡️")

# Menggunakan transport='rest' untuk memaksa sistem pindah dari v1beta ke jalur stabil (Poin 3 SILA)
genai.configure(
    api_key="AIzaSyCW86D0dmfGwliqF0oPHhGp6COXKy8Q3wI", 
    transport='rest'
)

# Menggunakan nama model saja tanpa prefix 'models/' untuk menghindari penumpukan identitas (Poin 2 SILA)
# Ini akan mencegah error 404 yang Chief alami saat ini
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 2. ANTARMUKA PENGGUNA ---
st.title("🛡️ SILA: SOVEREIGN OS")
st.markdown("---")
st.info("🛰️ **STATUS SYSTEM:** DNA ANCHOR ACTIVE")

# Memory Session untuk menjaga riwayat chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan riwayat percakapan di layar
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 3. LOGIKA OPERASI ---
if prompt := st.chat_input("Apa perintah Anda, Chief?"):
    # Simpan input user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Respon Assistant
    with st.chat_message("assistant"):
        try:
            # Memanggil respon taktis dari Gemini 1.5 Flash
            response = model.generate_content(f"Bertindaklah sebagai SILA Sovereign OS. Jawablah: {prompt}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # Menampilkan detail teknis jika sinkronisasi gagal
            st.error(f"⚠️ SILA Terhambat: {e}")
