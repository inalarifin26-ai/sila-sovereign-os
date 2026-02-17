import streamlit as st

st.title("🕶️ SILA: Secret Diagnostic")

# Cek apakah ada secrets sama sekali
if not st.secrets:
    st.error("SISTEM BUTA: Tidak ada Secrets yang terdeteksi sama sekali di Dashboard Streamlit.")
else:
    st.success("SISTEM MELIHAT SESUATU: Ada Secrets yang terdeteksi.")
    # Tampilkan daftar kunci yang tersedia (HANYA KUNCINYA, BUKAN ISINYA)
    st.write("Kunci yang terdaftar di sistem Anda:")
    for key in st.secrets.keys():
        st.code(key)
    
    if "GOOGLE_API_KEY" in st.secrets:
        st.success("TARGET DITEMUKAN: GOOGLE_API_KEY sudah ada di tempatnya.")
        st.info("Silakan ganti kembali ke kode chat sebelumnya.")
    else:
        st.warning("TARGET MISSED: GOOGLE_API_KEY tidak ditemukan dalam daftar di atas.")

st.write("---")
st.write("Pastikan di Dashboard Streamlit > Settings > Secrets, Anda menulisnya seperti ini:")
st.code('GOOGLE_API_KEY = "AIzaSy..."')
