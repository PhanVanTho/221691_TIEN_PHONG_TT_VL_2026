import os
import requests
import sys
from dotenv import load_dotenv

def test_endpoint(url, key, name):
    print(f"\nChecking {name}...")
    try:
        r = requests.get(f"{url}?key={key}", timeout=10)
        print(f"  Status: {r.status_code}")
        if r.status_code == 200:
            models = [m['name'] for m in r.json().get('models', [])]
            print(f"  Found {len(models)} models.")
            print(f"  Available: {', '.join(models[:3])}...")
            return True
        else:
            print(f"  Error: {r.text}")
    except Exception as e:
        print(f"  Exception: {e}")
    return False

def main():
    load_dotenv()
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        print("❌ ERROR: GEMINI_API_KEY not found in .env")
        return

    print(f"API Key found: {key[:4]}...{key[-4:]}")

    # Endpoints to check
    endpoints = [
        ("https://generativelanguage.googleapis.com/v1/models", "V1 Endpoint"),
        ("https://generativelanguage.googleapis.com/v1beta/models", "V1Beta Endpoint")
    ]

    ok = False
    for url, name in endpoints:
        if test_endpoint(url, key, name):
            ok = True

    if ok:
        print("\n✅ API connection is functional on at least one endpoint.")
        print("The system has been updated to use REST fallback if the SDK fails.")
    else:
        print("\n❌ API connection failed on all endpoints. Please check your API key and internet connection.")

if __name__ == "__main__":
    main()
