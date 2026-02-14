import streamlit as st
import google.generativeai as genai
import firebase_admin
from firebase_admin import credentials, firestore
import json

# 1. SETUP FIREBASE
if not firebase_admin._apps:
    try:
        key_dict = json.loads(st.secrets["FIREBASE_JSON"])
        cred = credentials.Certificate(key_dict)
        firebase_admin.initialize_app(cred)
    except Exception as e:
        st.error(f"Error Firebase: {e}")

db = firestore.client()

# 2. SETUP GEMINI (MENGGUNAKAN MODEL TERBARU DARI AI STUDIO)
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Berdasarkan cross-check AI Studio kamu
# Kita gunakan model yang paling stabil saat ini
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="Pabrik Konten AI")
st.title("🚀 Pabrik Konten AI")

# 3. SISTEM LOGIN & SALDO FIRESTORE
user_id = st.text_input("Masukkan ID User Anda", value="user_01")

if user_id:
    # Mengambil dokumen 'user_01' dari koleksi 'user'
    user_ref = db.collection('user').document(user_id)
    doc = user_ref.get()

    if doc.exists:
        user_data = doc.to_dict()
        saldo = user_data.get('saldo', 0)
        
        st.sidebar.title(f"💰 Saldo: {saldo} Poin")
        st.sidebar.write(f"User: {user_id}")

        topik = st.text_area("Apa yang ingin kamu buat?")
        
        if st.button("Buat Konten (50 Poin)"):
            if saldo >= 50:
                with st.spinner('Sedang memproses...'):
                    try:
                        # Memanggil AI dengan model terbaru
                        response = model.generate_content(topik)
                        st.markdown("### Hasil:")
                        st.write(response.text)
                        
                        # Potong saldo otomatis di Firestore
                        new_saldo = int(saldo) - 50
                        user_ref.update({'saldo': new_saldo})
                        st.success(f"Berhasil! Sisa Saldo: {new_saldo}")
                        st.balloons()
                    except Exception as e:
                        st.error(f"Gagal memanggil AI: {e}")
            else:
                st.error("Saldo tidak cukup!")
    else:
        st.error("ID User tidak ditemukan.")
