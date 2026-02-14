import streamlit as st
import google.generativeai as genai
import firebase_admin
from firebase_admin import credentials, firestore
import json
from datetime import datetime

# --- 1. SETUP FIREBASE ---
if not firebase_admin._apps:
    try:
        key_dict = json.loads(st.secrets["FIREBASE_JSON"])
        cred = credentials.Certificate(key_dict)
        firebase_admin.initialize_app(cred)
    except Exception as e:
        st.error(f"Error Firebase: {e}")
db = firestore.client()

# --- 2. SETUP GEMINI AI ---
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
target_model = next((m for m in available_models if 'flash' in m), available_models[0])
model = genai.GenerativeModel(target_model)

st.set_page_config(page_title="Pabrik Konten AI", layout="wide")

# --- 3. LOGIKA RESET HARIAN & LOGIN ---
st.sidebar.title("🚀 Menu Akses")
menu = ["Login", "Daftar Akun Baru"]
choice = st.sidebar.selectbox("Pilih Tindakan", menu)

today_date = datetime.now().strftime("%Y-%m-%d")

if choice == "Daftar Akun Baru":
    st.title("📝 Pendaftaran User Baru")
    new_user = st.text_input("Buat ID User", placeholder="Contoh: creator_budi")
    if st.button("Daftar Sekarang"):
        user_ref = db.collection('user').document(new_user)
        if user_ref.get().exists:
            st.error("ID sudah ada!")
        else:
            # Pendaftaran pertama langsung kasih 250 poin & catat tanggal
            user_ref.set({
                'saldo': 250, 
                'terakhir_akses': today_date
            })
            st.success("Berhasil! Jatah 5 konten hari ini sudah aktif.")
            st.balloons()

elif choice == "Login":
    user_id = st.text_input("Masukkan ID User Anda", value="user_01")
    if user_id:
        user_ref = db.collection('user').document(user_id)
        doc = user_ref.get()

        if doc.exists:
            user_data = doc.to_dict()
            saldo = user_data.get('saldo', 0)
            last_date = user_data.get('terakhir_akses', "")

            # LOGIKA RESET OTOMATIS: Jika hari ini beda dengan tanggal terakhir login
            if last_date != today_date:
                saldo = 250 # Reset jadi 5 konten (250 poin)
                user_ref.update({
                    'saldo': saldo,
                    'terakhir_akses': today_date
                })
                st.info("🎁 Jatah 5 konten gratis kamu hari ini sudah diperbarui!")

            # --- TAMPILAN DASHBOARD ---
            st.sidebar.markdown(f"### 💰 Saldo: **{saldo} Poin**")
            st.sidebar.write(f"📅 Tanggal: {today_date}")
            
            # --- HALAMAN UTAMA ---
            st.title("🤖 Pabrik Konten AI")
            topik = st.text_area("Apa ide kontenmu?")
            
            if st.button("Generate (50 Poin)"):
                if saldo >= 50:
                    with st.spinner('Meracik konten...'):
                        response = model.generate_content(topik)
                        st.markdown("### ✨ Hasil:")
                        st.write(response.text)
                        
                        # Potong Saldo
                        new_saldo = saldo - 50
                        user_ref.update({'saldo': new_saldo})
                        st.success(f"Sisa jatah: {new_saldo // 50} konten hari ini.")
                        
                        # FITUR SURVEY
                        st.divider()
                        st.write("📊 **Survey Singkat:** Seberapa puas kamu?")
                        feedback = st.select_slider("Rating:", options=["Buruk", "Biasa", "Mantap!"])
                        if st.button("Kirim Feedback"):
                            db.collection('feedback').add({
                                'user': user_id,
                                'rating': feedback,
                                'tanggal': today_date
                            })
                            st.toast("Terima kasih!")
                else:
                    st.error("Jatah gratis hari ini habis. Sampai jumpa besok!")
        else:
            st.error("User tidak ditemukan.")
