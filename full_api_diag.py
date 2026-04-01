import os
print("--- SCRIPT STARTED ---")
import requests
from dotenv import load_dotenv

def diag():
    load_dotenv()
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        print("GEMINI_API_KEY not found")
        return

    print(f"API Key: {key[:10]}...{key[-5:]}")
    
    endpoints = [
        "https://generativelanguage.googleapis.com/v1/models",
        "https://generativelanguage.googleapis.com/v1beta/models"
    ]
    
    for url in endpoints:
        print(f"\n--- Testing Endpoint: {url} ---")
        try:
            r = requests.get(f"{url}?key={key}")
            print(f"Status: {r.status_code}")
            if r.status_code == 200:
                models = r.json().get("models", [])
                print(f"Success! Found {len(models)} models.")
                # List first 5 models
                for m in models[:5]:
                    print(f" - {m['name']}")
                
                # Try a small generation on v1 for gemini-1.5-flash
                if "v1" in url:
                    gen_url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={key}"
                    payload = {"contents": [{"parts":[{"text": "Translate to Vietnamese: Hello"}]}]}
                    resp = requests.post(gen_url, json=payload)
                    print(f"Generation Test (gemini-1.5-flash): {resp.status_code}")
                    if resp.status_code == 200:
                        print(f"Response: {resp.json()['candidates'][0]['content']['parts'][0]['text']}")
            else:
                print(f"Error: {r.text}")
        except Exception as e:
            print(f"Exception: {e}")

if __name__ == "__main__":
    diag()
