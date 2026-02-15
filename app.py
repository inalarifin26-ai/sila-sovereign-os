import streamlit as st
import google.generativeai as genai

# 1. Setting Halaman
st.set_page_config(page_title="NOFA Factory", layout="wide")

# 2. Ambil Kunci Baru dari Secrets
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Kunci API belum dipasang di Secrets!")

# 3. Mesin AI "Sapu Jagat" (Mencoba semua model yang mungkin)
def panggil_ai_aman(prompt):
    # Urutan model: yang terbaru (flash) sampai yang stabil (pro)
    model_list = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
    for nama_model in model_list:
        try:
            model = genai.GenerativeModel(nama_model)
            response = model.generate_content(prompt)
            return response.text
        except:
            continue # Jika gagal 404, coba model berikutnya di daftar
    return None

# 4. Logika Menu (Session State)
if 'step' not in st.session_state:
    st.session_state.step = "login"

# --- TAMPILAN ---

if st.session_state.step == "login":
    st.title("🔑 Studio Access")
    uid = st.text_input("Creator ID", value="user_01")
    st.subheader(f"🤖 Halo, {uid}!")
    input_user = st.text_area("Request Konten Anda:")
    
    if st.button("⚡ GENERATE"):
        with st.spinner("Menghubungkan ke server AI..."):
            hasil = panggil_ai_aman(input_user)
            if hasil:
                st.session_state.hasil = hasil
                st.session_state.step = "dashboard"
                st.rerun()
            else:
                st.error("Gagal! Semua model AI (Flash/Pro) merespon 404. Pastikan API Key sudah benar-benar aktif di Google AI Studio.")

else:
    # DASHBOARD UTAMA DENGAN NAVIGASI BAWAH
    st.markdown("### 🧬 NOFA FACTORY V1.0.42")
    
    # Membuat tab navigasi yang Manajer inginkan
    t1, t2, t3, t4 = st.tabs(["🏠 HOME", "📝 PRODUKSI", "🎨 EDITOR", "📚 GUDANG"])
    
    with t1:
        st.success("Produksi Berhasil!")
        st.write(st.session_state.hasil)
    
    with t2:
        st.subheader("Pusat Produksi")
        st.write("Silakan pilih target media:")
        st.button("Sosial Media")
        st.button("Blog/Artikel")
        
    with t3:
        st.info("Fitur Editor Gambar segera hadir.")
        
    with t4:
        st.write("Neural Vault Anda tersimpan aman.")

    if st.button("⬅️ Kembali"):
        st.session_state.step = "login"
        st.rerun()
