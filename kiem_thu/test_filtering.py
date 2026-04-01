from ung_dung.xu_ly_ai.xu_ly_noi_dung import loc_cac_doan_rac, check_relevance, phan_loai_noi_dung

def test_filtering_logic():
    topic = "Trí tuệ nhân tạo"
    
    print(f"=== TESTING FILTERING FOR TOPIC: {topic} ===\n")
    
    # 1. Test check_relevance
    test_paragraphs = [
        ("Trí tuệ nhân tạo (AI) là một lĩnh vực của khoa học máy tính.", "High relevance"),
        ("Trường Đại học Công nghệ thông tin có khuôn viên rất đẹp.", "Low relevance"),
        ("Bạn có thể xem thêm tại bài viết gốc trên Wikipedia.", "Meta/Trash"),
        ("Vào năm 1956, hội nghị Dartmouth đã đặt nền móng cho AI.", "Medium relevance (History)"),
        ("AI được ứng dụng trong y tế để chẩn đoán bệnh.", "Medium relevance (Application)"),
        ("See also: Machine Learning.", "Meta/Trash (English)")
    ]
    
    print("--- 1. Testing Relevance Scoring ---")
    for p, desc in test_paragraphs:
        score = check_relevance(p, topic)
        print(f"[{score}] {desc}: {p[:50]}...")
        
    # 2. Test loc_cac_doan_rac
    print("\n--- 2. Testing Logic Filter (loc_cac_doan_rac) ---")
    input_list = [p[0] for p in test_paragraphs]
    # Add some short trash
    input_list.append("Ngắn quá.") 
    input_list.append("Liên kết ngoài http://google.com")
    
    clean_list = loc_cac_doan_rac(input_list, topic=topic)
    print(f"Input size: {len(input_list)}")
    print(f"Output size: {len(clean_list)}")
    print("Kept paragraphs:")
    for p in clean_list:
        print(f" - {p}")
        
    # 3. Test Classification with Topic
    print("\n--- 3. Testing Classification with Topic Context ---")
    clean_list.append("Năm 2023 đánh dấu sự bùng nổ của Generative AI.")
    classification = phan_loai_noi_dung(clean_list, chu_de=topic)
    
    for cat, items in classification.items():
        if items:
            print(f"Category [{cat.upper()}]: {len(items)} items")
            for item in items:
                print(f"  > {item[:60]}...")

if __name__ == "__main__":
    test_filtering_logic()
