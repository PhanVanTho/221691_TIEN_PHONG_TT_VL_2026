import os
import time
import re
import json
import requests
from dotenv import load_dotenv

load_dotenv()

# Model mặc định cho năm 2026 (Model 1.5 đã hết hạn gây 404)
# Chúng ta dùng 2.0-flash vì log xác định nó khả dụng (trả về 429 thay vì 404)
ACTIVE_MODEL_NAME = "gemini-2.0-flash"

def cau_hinh_gemini():
    """Kiểm tra cấu hình Gemini API key"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("⚠ WARNING: GEMINI_API_KEY not found in env.")
        return False
    return True

def goi_gemini_rest(prompt: str, model_name: str = ACTIVE_MODEL_NAME) -> str:
    """
    Gọi Gemini API trực tiếp qua REST (thử v1 rồi v1beta).
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None
        
    full_model_name = f"models/{model_name}" if not model_name.startswith("models/") else model_name
    
    # Danh sách endpoint thử nghiệm
    urls = [
        f"https://generativelanguage.googleapis.com/v1/{full_model_name}:generateContent?key={api_key}",
        f"https://generativelanguage.googleapis.com/v1beta/{full_model_name}:generateContent?key={api_key}"
    ]
    
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.2, "maxOutputTokens": 4096}
    }
    
    for url in urls:
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            if response.status_code == 200:
                data = response.json()
                if 'candidates' in data and len(data['candidates']) > 0:
                    return data['candidates'][0]['content']['parts'][0]['text'].strip()
            elif response.status_code == 429:
                print(f"⚠ QUOTA EXHAUSTED (429) for {model_name}. Please wait a few minutes.")
                return "ERR_QUOTA"
            elif response.status_code == 404:
                continue # Thử endpoint tiếp theo
            else:
                print(f"  [REST] Error {response.status_code} at {url}: {response.text}")
        except Exception as e:
            print(f"  [REST] Exception: {e}")
            
    return None

def dich_sang_tieng_viet(text: str) -> str:
    """Dịch văn bản đơn lẻ"""
    if not text or len(text.strip()) < 2:
        return text

    if not cau_hinh_gemini():
        return text

    prompt = f"""
    Dịch văn bản giáo trình sau sang TIẾNG VIỆT HOÀN TOÀN. 
    Văn phong hàn lâm, chuyên nghiệp. Giữ nguyên HTML.
    Văn bản: {text}
    """
    
    print(f"[AI-REST] Dang dich ({len(text)} ky tu)...")
    res = goi_gemini_rest(prompt)
    
    if res == "ERR_QUOTA":
        return text # Trả về bản gốc nếu hết quota
    return res if res else text

def dich_danh_sach_doan(danh_sach_doan: list) -> list:
    """Dịch batch qua JSON"""
    if not danh_sach_doan:
        return []
        
    if not cau_hinh_gemini():
        return danh_sach_doan

    input_data = {str(i): doan for i, doan in enumerate(danh_sach_doan)}
    input_json = json.dumps(input_data, ensure_ascii=False)
    
    prompt = f"Dịch các giá trị JSON sau sang TIẾNG VIỆT, trả về JSON chuẩn:\n{input_json}"
    
    print(f"  -> [AI-REST] Dang dich batch {len(danh_sach_doan)} doan...")
    content = goi_gemini_rest(prompt)
    
    if content == "ERR_QUOTA":
        return danh_sach_doan
        
    if content:
        match = re.search(r'\{.*\}', content, re.DOTALL)
        if match:
            try:
                translated_data = json.loads(match.group(0))
                return [translated_data.get(str(i), danh_sach_doan[i]) for i in range(len(danh_sach_doan))]
            except: pass
            
    # Fallback: Dịch từng đoạn (chỉ khi không lỗi quota)
    return [dich_sang_tieng_viet(doan) for doan in danh_sach_doan]
