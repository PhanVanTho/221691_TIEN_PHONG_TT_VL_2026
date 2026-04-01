import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

def run_diag():
    with open("diag_output.txt", "w", encoding="utf-8") as f:
        f.write("--- INTERNAL DIAGNOSTIC START ---\n")
        key = os.getenv("GEMINI_API_KEY")
        if not key:
            f.write("ERROR: GEMINI_API_KEY not found\n")
            return

        f.write(f"Key: {key[:8]}...\n")
        
        # Test internet
        try:
            ip = requests.get("https://api.ipify.org", timeout=5).text
            f.write(f"Internet: OK (IP: {ip})\n")
        except Exception as e:
            f.write(f"Internet: FAILED ({e})\n")

        # Try ListModels on v1 and v1beta
        endpoints = [
            "https://generativelanguage.googleapis.com/v1/models",
            "https://generativelanguage.googleapis.com/v1beta/models"
        ]
        
        for url in endpoints:
            f.write(f"\nEndpoint: {url}\n")
            try:
                r = requests.get(f"{url}?key={key}", timeout=10)
                f.write(f"Status: {r.status_code}\n")
                if r.status_code == 200:
                    models = r.json().get("models", [])
                    f.write(f"Found {len(models)} models\n")
                    for m in models:
                        f.write(f" - {m['name']}\n")
                else:
                    f.write(f"Error Body: {r.text}\n")
            except Exception as e:
                f.write(f"Exception: {e}\n")
        
        f.write("\n--- END ---\n")

if __name__ == "__main__":
    run_diag()
