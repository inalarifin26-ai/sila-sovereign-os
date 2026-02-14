import streamlit as st
import google.generativeai as genai
import firebase_admin
from firebase_admin import credentials, db
import json

# 1. SETUP FIREBASE
if not firebase_admin._apps:
    # Data diambil dari Secrets di Streamlit Cloud
    key_dict = json.loads(st.secrets["FIREBASE_JSON"])
    cred = credentials.Certificate(key_dict)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://value-fe222-default-rtdb.firebaseio.com/'
    })

# 2. SETUP GEMINI AI
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-pro')

st.set_page_config(page_title="Pabrik Konten AI", page_icon="🚀")
st.title("🚀 Pabrik Konten AI")

# 3. SISTEM LOGIN & SALDO
user_id = st.text_input("Masukkan ID User Anda (Contoh: user_01)")

if user_id:
    ref = db.reference(f'users/{user_id}')
    user_data = ref.get()

    if user_data:
        saldo = user_data.get('saldo', 0)
        st.sidebar.subheader(f"👤 User: {user_id}")
        st.sidebar.write(f"💰 Saldo: {saldo} Poin")

        # 4. FORM PEMBUAT KONTEN
        topik = st.text_area("Apa yang ingin kamu buat hari ini?", placeholder="Contoh: Tips sukses jualan online")
        
        if st.button("Buat Konten (Biaya: 50 Poin)"):
            if saldo >= 50:
                with st.spinner('AI sedang menulis konten untukmu...'):
                    try:
                        # Proses AI
                        response = model.generate_content(f"Buatlah konten sosial media yang menarik tentang: {topik}")
                        st.success("Konten Berhasil Dibuat!")
                        st.write(response.text)
                        
                        # Potong Saldo di Firebase
                        new_saldo = saldo - 50
                        ref.update({'saldo': new_saldo})
                        st.info(f"Saldo dipotong 50. Sisa saldo: {new_saldo}")
                        st.balloons()
                    except Exception as e:
                        st.error(f"Terjadi kesalahan AI: {e}")
            else:
                st.error("Saldo tidak cukup! Silakan hubungi admin untuk Top-up.")
    else:
        st.error("ID User tidak ditemukan. Pastikan sudah terdaftar di database.")
else:
    st.info("Silakan masukkan ID User di kolom atas untuk mulai.")
