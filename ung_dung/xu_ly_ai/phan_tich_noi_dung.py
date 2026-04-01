def tao_cau_truc_giao_trinh(noi_dung: str) -> dict:
    """
    Tạo cấu trúc giáo trình 6 mục từ nội dung văn bản
    (phiên bản rule-based, dùng cho luận văn & kiểm thử)
    """

    doan = [d.strip() for d in noi_dung.split("\n") if len(d.strip()) > 50]

    return {
        "1. Khái niệm": doan[0:3],
        "2. Lịch sử phát triển": doan[3:6],
        "3. Thành phần và nguyên lý": doan[6:9],
        "4. Quy trình hoạt động": doan[9:12],
        "5. Ứng dụng thực tiễn": doan[12:15],
        "6. Đánh giá và xu hướng": doan[15:18]
    }
