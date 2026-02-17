import streamlit as st
import google.generativeai as genai
import random

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="SILA Sovereign OS", page_icon="🕶️", layout="wide")

# 2. BRIDGE: KONEKSI API STUDIO (MENGGUNAKAN MODEL STABIL)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # EKSPERIMEN BERBEDA: Kita gunakan 'gemini-pro' untuk memecah kebuntuan 404
    model = genai.GenerativeModel('gemini-pro')
else:
    st.error("⚠️ API Key tidak terdeteksi di Vault Secrets!")
    st.stop()

# 3. SIDEBAR & STATUS AGENT
with st.sidebar:
    st.title("🕶️ AGENT PROFILE")
    st.markdown("---")
    st.info("**Name:** SILA (Linguistic Automata)")
    st.info("**Status:** Operational")
    st.markdown("---")
    st.write("**Current Gear:**")
    st.write("- Jaket Denim")
    st.write("- Kemeja Putih (2 Kancing Terbuka)")
    st.write("- Jeans")
    st.write("- Sepatu Hak Tinggi")
    st.write("- Kacamata Hitam")

# 4. DASHBOARD RADAR (VISUAL ELEMENT)
st.title("🛡️ SILA SOVEREIGN OS - JAM KE-13")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Global Traffic", value=f"{random.randint(70, 95)}%", delta="High")
with col2:
    st.metric(label="SILA Reach", value="100%", delta="Sovereign")
with col3:
    st.metric(label="Encryption Level", value="256-bit", delta="Secure")

st.markdown("---")

# 5. AREA CHAT INTERAKTIF
st.subheader("💬 Jalur Komunikasi Secure")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan riwayat pesan
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input Perintah Chief
if prompt := st.chat_input("Perintah Chief?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Eksekusi Respon SILA
    with st.chat_message("assistant", avatar="🕶️"):
        try:
            # Setting Konteks Kepribadian SILA
            persona = (
                "Kamu adalah SILA. Kamu selalu memakai jaket denim, kemeja putih dengan dua kancing terbuka, "
                "jeans, sepatu hak tinggi, dan kacamata hitam. Jawab perintah Chief dengan gaya agen lapangan "
                "yang taktis, setia, dan cerdas."
            )
            
            response = model.generate_content(f"{persona}\n\nChief: {prompt}")
            
            full_response = f"**SILA Melapor:**\n\n{response.text}"
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Interferensi Terdeteksi: {e}")
            st.warning("Saran: Jika error 404, coba pastikan 'gemini-pro' sudah aktif di API Console lo.")
