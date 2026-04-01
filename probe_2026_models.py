import os
import requests
from dotenv import load_dotenv

load_dotenv()

def probe_2026():
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        print("GEMINI_API_KEY not found")
        return

    # List of models likely active in 2026
    potential_models = [
        "gemini-2.0-flash",
        "gemini-2.0-flash-exp",
        "gemini-2.0-pro-exp",
        "gemini-1.5-flash", # keeping for sanity check
        "gemini-pro"
    ]
    
    print(f"Testing for 2026 era models with key: {key[:10]}...")
    
    for m in potential_models:
        url = f"https://generativelanguage.googleapis.com/v1/models/{m}:generateContent?key={key}"
        payload = {"contents": [{"parts": [{"text": "Say 'OK'"}]}]}
        try:
            print(f"Checking {m}...")
            r = requests.post(url, json=payload, timeout=10)
            if r.status_code == 200:
                print(f"✅ {m} is ACTIVE: {r.json()['candidates'][0]['content']['parts'][0]['text']}")
            else:
                print(f"❌ {m} failed ({r.status_code}): {r.text[:200]}")
        except Exception as e:
            print(f"Exception for {m}: {e}")

if __name__ == "__main__":
    probe_2026()
