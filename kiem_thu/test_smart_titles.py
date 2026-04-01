from ung_dung.xu_ly_ai.xu_ly_noi_dung import tao_tieu_de_doan, tim_tu_khoa_pho_bien

def test_smart_titles():
    print("=== TESTING SMART TITLE GENERATION ===\n")

    # Case 1: Definition Heuristic (Should still work)
    p1 = "Học máy là một lĩnh vực của trí tuệ nhân tạo."
    t1 = tao_tieu_de_doan(p1, "AI")
    print(f"1. Definition:\n   Input: {p1}\n   Output: {t1}\n   Expected: Khái niệm và định nghĩa\n")

    # Case 2: History Heuristic
    p2 = "Vào năm 1950, Alan Turing đã đề xuất phép thử Turing."
    t2 = tao_tieu_de_doan(p2, "AI")
    print(f"2. History:\n   Input: {p2}\n   Output: {t2}\n   Expected: Dấu mốc lịch sử năm 1950\n")

    # Case 3: Keyword Extraction (Recurring keyword)
    # Paragraph talking about LSTM without explicit definition structure
    p3 = "Mạng LSTM có khả năng ghi nhớ thông tin dài hạn. LSTM giải quyết vấn đề biến mất gradient. Kiến trúc của LSTM bao gồm các cổng quên và cổng nhập. LSTM rất phổ biến trong xử lý ngôn ngữ tự nhiên."
    t3 = tao_tieu_de_doan(p3, "Deep Learning")
    print(f"3. Keyword Extraction:\n   Input: {p3[:50]}...\n   Key found: {tim_tu_khoa_pho_bien(p3)}\n   Output: {t3}\n   Expected: Tìm hiểu về Lstm (or similar)\n")

    # Case 4: Fallback (generic text)
    p4 = "Đây là một đoạn văn bình thường không có cấu trúc đặc biệt và cũng không lặp lại từ khóa nào quá nhiều."
    t4 = tao_tieu_de_doan(p4, "General")
    print(f"4. Fallback:\n   Input: {p4}\n   Output: {t4}\n   Expected: (First few words...)\n")
    
    # Case 5: Complex Definition cleanup
    p5 = "Sự phát triển của Mạng nơ-ron nhân tạo là nền tảng của Deep Learning."
    t5 = tao_tieu_de_doan(p5, "AI")
    print(f"5. Complex Subject:\n   Input: {p5}\n   Output: {t5}\n   Expected: Mạng nơ-ron nhân tạo...\n")

if __name__ == "__main__":
    test_smart_titles()
