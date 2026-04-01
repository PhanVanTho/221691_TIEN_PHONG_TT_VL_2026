import os
import requests
from dotenv import load_dotenv

load_dotenv()

def list_models():
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        print("GEMINI_API_KEY not found")
        return

    print(f"Testing with API Key: {key[:10]}...")
    
    # Try public IP check to ensure internet
    try:
        ip = requests.get("https://api.ipify.org", timeout=5).text
        print(f"Internet connection OK. Public IP: {ip}")
    except:
        print("Internet connection appears DOWN or proxy restricted.")

    endpoints = [
        "https://generativelanguage.googleapis.com/v1/models",
        "https://generativelanguage.googleapis.com/v1beta/models"
    ]
    
    for url in endpoints:
        print(f"\n--- Listing models from: {url} ---")
        try:
            r = requests.get(f"{url}?key={key}", timeout=10)
            print(f"Status: {r.status_code}")
            if r.status_code == 200:
                data = r.json()
                models = data.get("models", [])
                print(f"Found {len(models)} models.")
                for m in models:
                    name = m.get("name")
                    methods = m.get("supportedGenerationMethods", [])
                    print(f" - {name} (Methods: {methods})")
            else:
                print(f"Error {r.status_code}: {r.text}")
        except Exception as e:
            print(f"Exception calling {url}: {e}")

if __name__ == "__main__":
    list_models()
