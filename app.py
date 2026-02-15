import streamlit as st
import google.generativeai as genai

# --- KONFIGURASI MESIN AI ---
# Menggunakan model terbaru agar tidak error 'NotFound'
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# --- SETTING TAMPILAN ---
st.set_page_config(page_title="NOFA Content Factory", layout="wide")

# Inisialisasi session state agar menu tidak hilang
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# --- FUNGSI GENERATE ---
def generate_ai_content(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Waduh, mesin mogok: {e}")
        return None

# --- LOGIKA TAMPILAN (UI) ---

# 1. TAMPILAN STUDIO ACCESS (Halaman Depan)
if not st.session_state.logged_in:
    st.title("🔑 Studio Access")
    user_id = st.text_input("Enter your Creator ID", value="user_01")
    st.subheader(f"🤖 Welcome back, {user_id}!")
    
    prompt = st.text_area("What's on your mind? (AI will craft the content for you)")
    
    if st.button("⚡ GENERATE"):
        with st.spinner("Sedang memasak konten..."):
            hasil = generate_ai_content(prompt)
            if hasil:
                st.session_state.logged_in = True
                st.session_state.hasil_konten = hasil
                st.rerun()

# 2. TAMPILAN PUSAT PRODUKSI (Setelah Generate Sukses)
else:
    # Header Aplikasi
    st.markdown("### 🧬 NOFA FACTORY V1.0.42")
    
    # Menu Navigasi Bawah (Gaya Aplikasi)
    menu = st.tabs(["🏠 HOME", "📝 PRODUKSI", "🎨 EDITOR", "📚 GUDANG"])
    
    with menu[0]:
        st.info("Pusat Produksi Aktif! Konten Viral hari ini siap diolah.")
        st.write(st.session_state.hasil_konten) # Menampilkan hasil generate tadi
        
    with menu[1]:
        st.subheader("Target Output")
        st.button("Sosial Media")
        st.button("Artikel/Blog")
        
    with menu[2]:
        st.subheader("Art Engine")
        st.write("Fitur Editor Gambar segera hadir.")
        
    with menu[3]:
        st.subheader("Neural Vault")
        st.write("Aset Anda tersimpan di sini.")

    if st.button("Keluar Studio"):
        st.session_state.logged_in = False
        st.rerun()
