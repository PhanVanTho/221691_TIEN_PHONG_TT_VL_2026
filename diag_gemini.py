import os
import google.generativeai as genai
from dotenv import load_dotenv

def run_diagnostic():
    print("=== GEMINI API DIAGNOSTIC ===")
    
    # 1. Check .env loading
    loaded = load_dotenv()
    print(f"1. .env file found and loaded: {loaded}")
    
    # 2. Check API Key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ 2. GEMINI_API_KEY NOT FOUND in environment.")
        return
    
    # Mask key for display
    masked_key = api_key[:5] + "..." + api_key[-5:] if len(api_key) > 10 else "***"
    print(f"2. GEMINI_API_KEY found: {masked_key}")
    print(f"   Key length: {len(api_key)}")
    
    # 3. Configure API
    try:
        genai.configure(api_key=api_key)
        print("3. genai.configure() succeeded.")
    except Exception as e:
        print(f"❌ 3. genai.configure() FAILED: {e}")
        return

    # 4. Check available models
    try:
        print("4. Listing available models...")
        models = genai.list_models()
        can_access_models = False
        for m in models:
            if 'generateContent' in m.supported_generation_methods:
                print(f"   - {m.name}")
                can_access_models = True
        if not can_access_models:
            print("❌ 4. No models supporting 'generateContent' found.")
    except Exception as e:
        print(f"❌ 4. Failed to list models: {e}")
        print("   (This usually means the API Key is invalid or has network restrictions)")

    # 5. Simple test prompt (gemini-1.5-flash)
    print("\n5. Testing translation with 'gemini-1.5-flash'...")
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Translate to Vietnamese: Hello World")
        if response and response.text:
            print(f"✅ 5. Success! Response: {response.text.strip()}")
        else:
            print("❌ 5. Failed: Empty response.")
    except Exception as e:
        print(f"❌ 5. FAILED: {e}")

    # 6. Simple test prompt (gemini-pro)
    print("\n6. Testing translation with 'gemini-pro'...")
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content("Translate to Vietnamese: Hello World")
        if response and response.text:
            print(f"✅ 6. Success! Response: {response.text.strip()}")
        else:
            print("❌ 6. Failed: Empty response.")
    except Exception as e:
        print(f"❌ 6. FAILED: {e}")

if __name__ == "__main__":
    run_diagnostic()
