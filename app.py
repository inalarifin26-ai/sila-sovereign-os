import streamlit as st
import google.generativeai as genai

# --- 1. KONFIGURASI DASAR ---
st.set_page_config(page_title="NOFA Factory", layout="wide")

# --- 2. KONEKSI MESIN AI (STABIL) ---
# Menggunakan 'gemini-pro' agar tidak muncul error 404
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-pro')

# Cek status login
if 'step' not in st.session_state:
    st.session_state.step = "login"

# --- 3. FUNGSI PENGOLAH KONTEN ---
def jalankan_ai(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Mesin AI bermasalah: {e}")
        return None

# --- 4. LOGIKA TAMPILAN (UI) ---

# TAMPILAN AWAL (LOGIN/ACCESS)
if st.session_state.step == "login":
    st.title("🔑 Studio Access")
    creator_id = st.text_input("Enter your Creator ID", value="user_01")
    st.subheader(f"🤖 Welcome back, {creator_id}!")
    
    ide_konten = st.text_area("Apa yang ingin Anda buat hari ini?")
    
    if st.button("⚡ GENERATE"):
        with st.spinner("Mengaktifkan Neural Network..."):
            hasil = jalankan_ai(ide_konten)
            if hasil:
                st.session_state.hasil = hasil
                st.session_state.step = "dashboard"
                st.rerun()

# TAMPILAN DASHBOARD (PUSAT PRODUKSI)
else:
    st.markdown("### 🧬 NOFA FACTORY V1.0.42")
    
    # Menu Navigasi Bawah yang Anda harapkan
    tab1, tab2, tab3, tab4 = st.tabs(["🏠 HOME", "📝 PRODUKSI", "🎨 EDITOR", "📚 GUDANG"])
    
    with tab1:
        st.success("✅ Produksi Selesai!")
        st.write(st.session_state.hasil)
        
    with tab2:
        st.subheader("Bahan Baku Konten")
        st.write("Silakan pilih target media Anda.")
        st.button("Sosial Media")
        st.button("Artikel/Blog")
        
    with tab3:
        st.subheader("Art Engine")
        st.info("Fitur editor sedang disinkronisasi.")
        
    with tab4:
        st.subheader("Neural Vault")
        st.write("Aset Anda tersimpan aman di sini.")

    if st.button("⬅️ Keluar ke Studio"):
        st.session_state.step = "login"
        st.rerun()
