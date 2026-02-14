import streamlit as st
import google.generativeai as genai
import firebase_admin
from firebase_admin import credentials, firestore
import json

# 1. SETUP FIREBASE FIRESTORE (Penyebab utama error jika salah kode)
if not firebase_admin._apps:
    try:
        key_dict = json.loads(st.secrets["FIREBASE_JSON"])
        cred = credentials.Certificate(key_dict)
        firebase_admin.initialize_app(cred)
    except Exception as e:
        st.error(f"Error Konfigurasi Secrets: {e}")

db = firestore.client()

# 2. SETUP GEMINI AI
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-pro')

st.set_page_config(page_title="Pabrik Konten AI", layout="centered")
st.title("🚀 Pabrik Konten AI")

# 3. SISTEM LOGIN & SALDO FIRESTORE
user_id = st.text_input("Masukkan ID User Anda", placeholder="Contoh: user_01")

if user_id:
    # Kode ini akan mencari di Koleksi 'user' dan Dokumen 'user_01' sesuai gambar 1000114587.jpg
    user_ref = db.collection('user').document(user_id)
    doc = user_ref.get()

    if doc.exists:
        user_data = doc.to_dict()
        saldo = user_data.get('saldo', 0)
        
        # Tampilan Sidebar untuk Saldo
        st.sidebar.subheader(f"👤 User: {user_id}")
        st.sidebar.title(f"💰 Saldo: {saldo} Poin")
        st.sidebar.divider()

        # Area Kerja Pembuatan Konten
        topik = st.text_area("Apa konten yang ingin kamu buat?", placeholder="Contoh: Buat caption jualan kopi...")
        
        if st.button("Buat Konten (Biaya: 50 Poin)"):
            if saldo >= 50:
                with st.spinner('AI sedang bekerja...'):
                    try:
                        response = model.generate_content(topik)
                        st.markdown("### Hasil Konten:")
                        st.write(response.text)
                        
                        # Update saldo otomatis di Firestore
                        new_saldo = saldo - 50
                        user_ref.update({'saldo': new_saldo})
                        
                        st.success(f"Berhasil! Saldo berkurang 50. Sisa: {new_saldo}")
                        st.balloons()
                        
                        # Tombol refresh manual jika sidebar tidak langsung update
                        if st.button("Refresh Saldo"):
                            st.rerun()
                    except Exception as e:
                        st.error(f"Gagal memanggil AI: {e}")
            else:
                st.error("Maaf, saldo kamu tidak cukup!")
    else:
        # Jika user mengetik ID selain user_01
        st.error(f"ID User '{user_id}' tidak ditemukan di database.")
else:
    st.info("Masukkan ID User (seperti user_01) untuk melihat saldo.")
