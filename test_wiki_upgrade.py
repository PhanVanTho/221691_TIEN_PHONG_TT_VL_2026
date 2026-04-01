from ung_dung.xu_ly_ai.wikipedia import lay_noi_dung_wikipedia
from ung_dung.xu_ly_ai.xu_ly_noi_dung import chia_doan, phan_loai_noi_dung

def test_wiki_en_and_links():
    topic = "Artificial Intelligence" # A topic with rich EN content
    print(f"Testing with topic: {topic}")
    
    # 1. Test fetching content
    content = lay_noi_dung_wikipedia(topic)
    print(f"\nTotal content length: {len(content)} chars")
    
    if "=== ENGLISH CONTENT" in content:
        print("[PASS] English content found.")
    else:
        print("[FAIL] English content NOT found.")
        
    if "--- RELATED:" in content:
        print("[PASS] Related links found.")
    else:
        print("[FAIL] Related links NOT found.")

    # 2. Test classification
    print("\nTesting classification...")
    updated_content = content.replace("=== ENGLISH CONTENT", "").replace("--- RELATED:", "") # Simple cleanup for test
    cac_doan = chia_doan(updated_content)
    phan_loai = phan_loai_noi_dung(cac_doan)
    
    print(f"Gioi thieu: {len(phan_loai['gioi_thieu'])} segments")
    print(f"Khai niem: {len(phan_loai['khai_niem'])} segments")
    print(f"Lich su: {len(phan_loai['lich_su'])} segments")
    print(f"Ung dung: {len(phan_loai['ung_dung'])} segments")
    
    if len(phan_loai['gioi_thieu']) > 0 or len(phan_loai['khai_niem']) > 0:
        print("[PASS] Classification works with English content.")
    else:
        print("[FAIL] Classification might not be catching English keywords.")

if __name__ == "__main__":
    test_wiki_en_and_links()
