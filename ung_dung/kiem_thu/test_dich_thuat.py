from ung_dung.xu_ly_ai.dich_thuat import dich_sang_tieng_viet, dich_danh_sach_doan
import os
from dotenv import load_dotenv

load_dotenv()

def test_translation():
    print("=== TEST TRANSLATION ===")
    
    # 1. Test single paragraph
    text_en = "Artificial Intelligence (AI) is the simulation of human intelligence processes by machines, especially computer systems."
    print(f"\n[Input]: {text_en}")
    text_vi = dich_sang_tieng_viet(text_en)
    print(f"[Output]: {text_vi}")
    
    if text_vi == text_en:
        print("⚠ WARNING: Text was not translated (or API failed).")
    else:
        print("✅ Translation seems to work.")

    # 2. Test list of paragraphs
    list_en = [
        "Machine learning is a subset of AI.",
        "It focuses on the use of data and algorithms to imitate the way that humans learn.",
        "Deep learning is part of a broader family of machine learning methods."
    ]
    print(f"\n[Input List]: {list_en}")
    list_vi = dich_danh_sach_doan(list_en)
    print(f"[Output List]: {list_vi}")

    if len(list_vi) == len(list_en) and list_vi[0] != list_en[0]:
         print("✅ List translation seems to work.")
    else:
         print("⚠ WARNING: List translation failed.")

if __name__ == "__main__":
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ GEMINI_API_KEY is missing!")
    else:
        test_translation()
