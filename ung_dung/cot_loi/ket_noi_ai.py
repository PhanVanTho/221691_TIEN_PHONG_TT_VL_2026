import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

# Cấu hình API key & Model (2026 era)
API_KEY = os.getenv("GEMINI_API_KEY")
ACTIVE_MODEL = "gemini-2.0-flash"

def goi_ai(prompt):
    """
    Hàm gọi AI chính qua REST (v1 sau đó v1beta)
    """
    if not API_KEY:
        return "⚠ Lỗi: Chưa cấu hình GEMINI_API_KEY trong file .env"
    
    full_model_name = f"models/{ACTIVE_MODEL}"
    urls = [
        f"https://generativelanguage.googleapis.com/v1/{full_model_name}:generateContent?key={API_KEY}",
        f"https://generativelanguage.googleapis.com/v1beta/{full_model_name}:generateContent?key={API_KEY}"
    ]
    
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 4096}
    }
    
    for url in urls:
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            if response.status_code == 200:
                data = response.json()
                if 'candidates' in data and len(data['candidates']) > 0:
                    return data['candidates'][0]['content']['parts'][0]['text']
            elif response.status_code == 429:
                return "⚠ Quota đã hết (429). Vui lòng thử lại sau vài phút."
            elif response.status_code == 404:
                continue
            else:
                return f"⚠ Lỗi {response.status_code}: {response.text}"
        except Exception as e:
            return f"⚠ Lỗi Exception: {str(e)}"
    
    return "⚠ Lỗi: Model không khả dụng (404 trên tất cả endpoint)"
