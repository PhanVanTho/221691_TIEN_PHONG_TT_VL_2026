from ung_dung.xu_ly_ai.tao_giao_trinh import tao_giao_trinh
import os
from dotenv import load_dotenv

load_dotenv()

def verify_full_translation():
    print("=== VERIFY FULL TRANSLATION ===")
    
    topic = "Quantum Computing"
    print(f"\nProcessing topic: {topic}...")
    
    result = tao_giao_trinh(topic)
    
    chu_de_vi = result.get("chu_de_vi", "")
    html = result.get("noi_dung", "")
    
    print(f"\n[Translated Topic Name]: {chu_de_vi}")
    
    if "Quantum Computing" in chu_de_vi:
        print("❌ FAILED: Main topic name was not translated.")
    else:
        print("✅ SUCCESS: Main topic name was translated.")
        
    # Check for English indicators in HTML (Commonly left untranslated if failure occurs)
    english_indicators = ["Chapter 1:", "OVERVIEW", "Topic Information", "Learning Objectives", "References"]
    found_en = [ind for ind in english_indicators if ind in html]
    
    if found_en:
        print(f"⚠ WARNING: Found potential English structural elements: {found_en}")
    else:
        print("✅ SUCCESS: No common English structural elements found in HTML.")

    # Check if content exists
    if len(html) > 1000:
        print(f"✅ SUCCESS: Curriculum generated ({len(html)} chars).")
    else:
        print("❌ FAILED: Curriculum content is too short or empty.")

if __name__ == "__main__":
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ GEMINI_API_KEY is missing!")
    else:
        verify_full_translation()
