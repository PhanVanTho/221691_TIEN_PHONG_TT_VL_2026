import os
import google.generativeai as genai
from dotenv import load_dotenv

def test_models():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY not found")
        return

    genai.configure(api_key=api_key)
    
    models_to_try = [
        "gemini-1.5-flash",
        "gemini-1.5-flash-latest",
        "gemini-pro",
        "gemini-1.0-pro",
        "gemini-1.5-pro",
        "models/gemini-1.5-flash",
        "models/gemini-pro"
    ]
    
    for model_name in models_to_try:
        print(f"Testing: {model_name}... ", end="", flush=True)
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Hi")
            if response:
                print("✅ SUCCESS!")
                return model_name
        except Exception as e:
            print(f"❌ FAILED ({str(e)[:100]}...)")
    
    return None

if __name__ == "__main__":
    test_models()
