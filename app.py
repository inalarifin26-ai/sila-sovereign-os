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

# 2. SETUP GEMINI DENGAN CARA BERBEDA (AUTO-DETECT MODEL)
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Kita tidak lagi mengetik manual nama modelnya agar tidak error 404
# Kode ini akan mencari model 'flash' apa pun yang tersedia di server saat ini
available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
target_model = next((m for m in available_models if 'flash' in m), available_models[0])
model = genai.GenerativeModel(target_model)

st.set_page_config(page_title="Pabrik Konten AI", layout="centered")
st.title("🚀 Pabrik Konten AI")

# 3. SISTEM LOGIN & SALDO
user_id = st.text_input("Masukkan ID User Anda", value="user_01")

if user_id:
    user_ref = db.collection('user').document(user_id)
    doc = user_ref.get()

    if doc.exists:
        user_data = doc.to_dict()
        saldo = user_data.get('saldo', 0)
        
        st.sidebar.title(f"💰 Saldo: {saldo} Poin")
        st.sidebar.write(f"👤 User: {user_id}")
        
        topik = st.text_area("Tulis ide kontenmu di sini...")
        
        if st.button("Buat Konten (50 Poin)"):
            if saldo >= 50:
                with st.spinner(f'Menggunakan model: {target_model}...'):
                    try:
                        # Cara pemanggilan yang lebih aman
                        response = model.generate_content(topik)
                        st.markdown("### Hasil Konten:")
                        st.write(response.text)
                        
                        # Update Saldo
                        new_saldo = int(saldo) - 50
                        user_ref.update({'saldo': new_saldo})
                        st.success(f"Berhasil! Sisa: {new_saldo}")
                        st.balloons()
                    except Exception as e:
                        st.error(f"AI sedang sibuk atau versi berubah: {e}")
            else:
                st.error("Saldo tidak cukup!")
    else:
        st.error("User tidak ditemukan.")
