# EKSPERIMEN BARU: Pakai model spesifik yang paling stabil di server lama
try:
    # Kita panggil dengan nama lengkap versinya
    model = genai.GenerativeModel('models/gemini-1.0-pro') 
    
    # Tes respons singkat
    response = model.generate_content("Cek Sinyal")
    st.write(response.text)
except Exception as e:
    st.error(f"Interferensi Sistem: {e}")
