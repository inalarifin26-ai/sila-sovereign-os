from fastapi import FastAPI
import uvicorn
import requests
import json

app = FastAPI()

# Alamat Ollama Lokal (Otak Genesis)
OLLAMA_URL = "http://localhost:11434/api/generate"

@app.get("/")
def status():
    return {"status": "GENESIS_ACTIVE", "identity": "SILA_SOVEREIGN_OS"}

@app.post("/ask")
async def ask_genesis(prompt: str):
    payload = {
        "model": "llama3", # Atau model yang Anda download
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(OLLAMA_URL, json=payload)
    return response.json()

if __name__ == "__main__":
    # KUNCI KEDAULATAN: host='0.0.0.0' membuat ini bisa diakses dari HP/Laptop lain
    # Port 8080 adalah gerbang masuknya
    uvicorn.run(app, host='0.0.0.0', port=8080)
