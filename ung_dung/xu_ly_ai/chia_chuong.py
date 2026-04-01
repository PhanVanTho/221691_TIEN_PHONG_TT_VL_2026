def chia_chuong_giao_trinh(noi_dung: str) -> dict:
    """
    Chia nội dung giáo trình thành các chương cơ bản
    dựa trên độ dài và từ khóa.
    """

    doan = [d.strip() for d in noi_dung.split("\n") if len(d.strip()) > 50]

    tong = len(doan)
    if tong < 5:
        return {"NOI_DUNG": noi_dung}

    c1 = "\n".join(doan[: tong // 5])
    c2 = "\n".join(doan[tong // 5 : 2 * tong // 5])
    c3 = "\n".join(doan[2 * tong // 5 : 3 * tong // 5])
    c4 = "\n".join(doan[3 * tong // 5 : 4 * tong // 5])
    c5 = "\n".join(doan[4 * tong // 5 :])

    return {
        "CHƯƠNG 1: GIỚI THIỆU": c1,
        "CHƯƠNG 2: KHÁI NIỆM VÀ ĐẶC ĐIỂM": c2,
        "CHƯƠNG 3: ỨNG DỤNG": c3,
        "CHƯƠNG 4: ƯU ĐIỂM VÀ HẠN CHẾ": c4,
        "CHƯƠNG 5: KẾT LUẬN": c5,
    }
