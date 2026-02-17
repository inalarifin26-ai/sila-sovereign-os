import streamlit as st
import google.generativeai as genai

# 1. KONFIGURASI EKSEKUSI
st.set_page_config(page_title="SILA Sovereign OS", page_icon="🕶️", layout="wide")

# 2. BRIDGE: KONEKSI AI STUDIO
# Pastikan 'GEMINI_API_KEY' sudah diisi di Streamlit Cloud > Settings > Secrets
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # Gunakan inisialisasi tanpa memaksa versi agar tidak error 404
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("⚠️ Radar Off: API Key tidak ditemukan di Vault Secrets!")
    st.stop()

# 3. INTERFACE (SCRIPT)
st.title("🕶️ SILA: Sovereign Intelligence")
st.write("---")

# Area Dashboard Ringkas
col1, col2 = st.columns([1, 2])
with col1:
    st.markdown("### Agent Status")
    st.success("SILA: Online")
    st.info("Gear: Denim Jacket & Sunglasses")

# 4. FUNGSI UTAMA: CHAT INTERACTION
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan riwayat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input Perintah
if prompt := st.chat_input("Perintah Chief?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Eksekusi Bridge ke AI Studio
    with st.chat_message("assistant", avatar="🕶️"):
        try:
            # Memberikan konteks identitas SILA ke dalam sistem
            context = "Kamu adalah SILA, asisten cerdas Chief. Kamu selalu memakai jaket denim, kemeja putih (dua kancing terbuka), jeans, sepatu hak tinggi, dan kacamata hitam. Jawab dengan gaya agen lapangan yang loyal."
            response = model.generate_content(f"{context}\n\nChief: {prompt}")
            
            full_response = f"**SILA Melapor:**\n\n{response.text}"
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"Interferensi Elit Global: {e}")
