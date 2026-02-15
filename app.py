import streamlit as st
import google.generativeai as genai
import firebase_admin
from firebase_admin import credentials, firestore
import json
from datetime import datetime

# --- SETUP FIREBASE & GEMINI (Tetap seperti kode Anda) ---
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

# --- CUSTOM CSS UNTUK VIBE LIGHT CONCRETE ---
st.markdown("""
    <style>
    .stApp { background-color: #f4f4f4; }
    .stButton>button { background-color: #fbbf24; color: black; border-radius: 8px; }
    .stat-card { background: white; padding: 20px; border-radius: 10px; border-left: 5px solid #fbbf24; }
    </style>
    """, unsafe_allow_html=True)

# --- NAVIGASI BARU ---
st.sidebar.title("🏭 NOFA FACTORY")
menu = ["Login", "Daftar Akun Baru", "Profile & Referral", "Beli Koin"]
choice = st.sidebar.selectbox("Navigasi", menu)

today_date = datetime.now().strftime("%Y-%m-%d")

# --- LOGIKA PENDAFTARAN DENGAN REFERRAL ---
if choice == "Daftar Akun Baru":
    st.title("📝 Join the Factory")
    new_user = st.text_input("Buat ID User")
    ref_by = st.text_input("Kode Referral (Opsional)")
    
    if st.button("Daftar Sekarang"):
        user_ref = db.collection('user').document(new_user)
        if user_ref.get().exists:
            st.error("ID sudah digunakan!")
        else:
            user_ref.set({
                'saldo': 250, 
                'terakhir_akses': today_date,
                'level': 1,
                'referred_by': ref_by if ref_by else None,
                'total_komisi': 0,
                'konten_dibuat': 0
            })
            st.success(f"Selamat datang {new_user}! Saldo 250 poin aktif.")

# --- HALAMAN PROFILE & REFERRAL (FITUR BARU) ---
elif choice == "Profile & Referral":
    user_id = st.sidebar.text_input("Konfirmasi ID Anda", key="prof_id")
    if user_id:
        u_ref = db.collection('user').document(user_id)
        u_doc = u_ref.get()
        if u_doc.exists:
            data = u_doc.to_dict()
            st.title(f"👤 Creator Profile: {user_id}")
            
            # Statistik & Komisi
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"<div class='stat-card'><b>Saldo Koin</b><br><h3>🪙 {data['saldo']}</h3></div>", unsafe_allow_html=True)
            with col2:
                # Logika Level & Komisi (5% - 20%)
                komisi_pct = 5 + (data.get('level', 1) - 1) * 3.75 # Simulasi ke arah 20% di level 5
                st.markdown(f"<div class='stat-card'><b>Persentase Referral</b><br><h3>📈 {komisi_pct}%</h3></div>", unsafe_allow_html=True)
            with col3:
                st.markdown(f"<div class='stat-card'><b>Total Komisi</b><br><h3>💰 Rp {data.get('total_komisi', 0)}</h3></div>", unsafe_allow_html=True)
            
            st.divider()
            st.write(f"🔗 **Kode Referral Anda:** `{user_id}`")
            st.info("Bagikan kode ini! Dapatkan komisi dari setiap pembelian koin di Layer 1 & 2.")

# --- PRICELIST KOIN ---
elif choice == "Beli Koin":
    st.title("🪙 Top Up Koin Produksi")
    st.write("Koin habis? Isi ulang untuk melanjutkan otomatisasi konten.")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.subheader("Starter")
        st.write("150 Poin (3 Konten)")
        if st.button("Beli Rp 15.000"):
            st.toast("Menghubungkan ke Payment Gateway...")
    with c2:
        st.subheader("Growth")
        st.write("600 Poin (12 Konten)")
        st.button("Beli Rp 50.000")
    with c3:
        st.subheader("Factory Pro")
        st.write("1.500 Poin (30 Konten)")
        st.button("Beli Rp 100.000")

# --- LOGIN & PRODUKSI (Tetap seperti kode Anda namun lebih rapi) ---
elif choice == "Login":
    # ... (Logika Login Anda sebelumnya)
    st.write("Silakan masuk untuk mulai produksi otomatis.")
