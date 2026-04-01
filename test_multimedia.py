from ung_dung.xu_ly_ai.wikipedia import lay_noi_dung_wikipedia

def test_multimedia():
    topic = "Machine Learning" 
    print(f"Testing multimedia fetch for: {topic}")
    
    data = lay_noi_dung_wikipedia(topic)
    
    print("\n--- RESULTS ---")
    if isinstance(data, dict):
        print(f"[PASS] Return type is dict.")
        print(f"Text length: {len(data.get('text', ''))}")
        
        images = data.get("images", [])
        print(f"Images found: {len(images)}")
        if images:
             print(f"Sample Image: {images[0]}")
        else:
             print("[WARN] No images found.")
             
        examples = data.get("examples", "")
        print(f"Examples length: {len(examples)}")
        if len(examples) > 100:
            print("[PASS] Examples found.")
        else:
            print("[WARN] Examples content is empty or short.")
            
    else:
        print(f"[FAIL] Return type is {type(data)}, expected dict.")

if __name__ == "__main__":
    test_multimedia()
