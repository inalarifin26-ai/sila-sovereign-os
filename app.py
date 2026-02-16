# Paksa pakai jalur v1 agar tidak kena 404 v1beta lagi
genai.configure(api_key=api_key, transport='rest') # Tambahkan transport='rest'

model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
)
