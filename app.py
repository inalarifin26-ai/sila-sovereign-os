import streamlit as st
import google.generativeai as genai
import firebase_admin
from firebase_admin import credentials, firestore
import json
from datetime import datetime

# --- 1. SETUP FIREBASE & GEMINI ---
if not firebase_admin._apps:
    try:
        key_dict = json.loads(st.secrets["FIREBASE_JSON"])
        cred = credentials.Certificate(key_dict)
        firebase_admin.initialize_app(cred)
    except Exception as e:
        st.error(f"Error Firebase: {e}")
db = firestore.client()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="NOFA FACTORY", layout="wide")

# --- 2. SIDEBAR NAVIGATION ---
st.sidebar.title("🏭 NOFA FACTORY")
menu = ["Login", "Daftar Akun Baru", "Profile & Referral", "Beli Koin"]
choice = st.sidebar.selectbox("Pilih Menu", menu)

today_date = datetime.now().strftime("%Y-%m-%d")

# --- 3. LOGIKA DAFTAR ---
if choice == "Daftar Akun Baru":
    st.title("📝 Pendaftaran Creator")
    new_user = st.text_input("Buat ID User (Tanpa Spasi)")
    ref_by = st.text_input("Kode Referral (Jika ada)")
    if st.button("Daftar Sekarang"):
        user_ref = db.collection('user').document(new_user)
        if user_ref.get().exists:
            st.error("ID sudah ada!")
        else:
            user_ref.set({
                'saldo': 250, 
                'terakhir_akses': today_date,
                'level': 1,
                'referred_by': ref_by if ref_by else None,
                'total_komisi': 0
            })
            st.success("Berhasil! Silakan kembali ke menu Login.")

# --- 4. LOGIKA LOGIN (Perbaikan agar tidak kosong) ---
elif choice == "Login":
    st.title("🔑 Masuk ke Dashboard")
    user_id = st.text_input("Masukkan ID User Anda", value="")
    
    if user_id:
        user_ref = db.collection('user').document(user_id)
        doc = user_ref.get()

        if doc.exists:
            user_data = doc.to_dict()
            saldo = user_data.get('saldo', 0)
            
            # Dashboard Utama Muncul Disini
            st.sidebar.success(f"Login: {user_id}")
            st.sidebar.markdown(f"### 💰 Saldo: **{saldo} Poin**")
            
            st.header("🤖 Pabrik Konten AI")
            topik = st.text_area("Apa ide kontenmu?")
            if st.button("Generate (50 Poin)"):
                if saldo >= 50:
                    with st.spinner('Memproses...'):
                        response = model.generate_content(topik)
                        st.markdown("### ✨ Hasil Konten:")
                        st.write(response.text)
                        # Potong saldo
                        user_ref.update({'saldo': saldo - 50})
                        st.rerun()
                else:
                    st.error("Koin habis! Silakan Top Up.")
        else:
            st.error("User tidak ditemukan.")
    else:
        st.info("Silakan ketik ID User Anda di atas untuk memulai.")

# --- 5. PROFILE & REFERRAL (Sistem 2-Layer 5-20%) ---
elif choice == "Profile & Referral":
    st.title("👤 Profile & Referral")
    user_id_check = st.text_input("Konfirmasi ID Anda untuk cek komisi")
    if user_id_check:
        u_doc = db.collection('user').document(user_id_check).get()
        if u_doc.exists:
            d = u_doc.to_dict()
            st.write(f"ID: **{user_id_check}** | Level: **{d.get('level', 1)}**")
            st.metric("Total Komisi", f"Rp {d.get('total_komisi', 0)}")
            st.info(f"Kode Referral Anda: {user_id_check}")
            st.write("Bagikan kode ini untuk dapat komisi 5% (Level 1) s/d 20% (Level 5)!")

# --- 6. BELI KOIN (Pricelist) ---
elif choice == "Beli Koin":
    st.title("🪙 Top Up Koin")
    col1, col2 = st.columns(2)
    with col1:
        st.write("📦 **Paket Hemat**")
        st.write("150 Poin (3 Konten)")
        st.button("Beli Rp 15.000")
    with col2:
        st.write("🔥 **Paket Pro**")
        st.write("600 Poin (12 Konten)")
        st.button("Beli Rp 50.000")
