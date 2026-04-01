import re


def lam_sach_van_ban(text: str) -> str:
    """
    Làm sạch văn bản từ Wikipedia một cách toàn diện.
    Loại bỏ ký tự lạ, rác mã hoá, và các phần không liên quan.
    """
    if not text:
        return ""

    # 1. Xóa tiêu đề wiki: == Tiêu đề ==, giữ lại nội dung
    text = re.sub(r"={2,}\s*(.*?)\s*={2,}", r"\n\1\n", text)

    # 2. Xóa phần liên kết tham khảo dạng [1], [2], [cần dẫn nguồn]
    text = re.sub(r"\[\d+\]", "", text)
    text = re.sub(r"\[cần dẫn nguồn\]", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\[cần chú thích\]", "", text, flags=re.IGNORECASE)
    # Xóa các link dạng [Link] hoặc [http...]
    text = re.sub(r"\[(http|www).*?\]", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\[.*?\]", "", text)  # Fallback: Xóa tất cả trong ngoặc vuông

    # 3. Xử lý lỗi encoding và ký tự lạ thường gặp (mojibake)
    # Ví dụ: â€œ -> ", â€ -> ", â€™ -> '
    replacements = {
        "â€œ": '"', "â€": '"', "â€™": "'", "â€“": "-", "â€”": "-",
        "â€¦": "...", "Ã": "à", "Ã³": "ó", "Ã¨": "è", "Ã©": "é",
        "Â": "",  # Remove random circumflex artifacts
    }
    for k, v in replacements.items():
        text = text.replace(k, v)

    # 4. Xóa các ký tự đặc biệt không mong muốn
    # Giữ lại các ký tự chữ cái (bao gồm tiếng Việt), số, và dấu câu thông dụng
    # Loại bỏ các ký tự điều khiển, emoji lạ, symbols vô nghĩa
    text = re.sub(r"[^\w\s.,?!:;\"\'\-\(\)%/àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ]", " ", text)
    
    # 5. Xóa các thẻ HTML/Wiki còn sót
    text = re.sub(r"'''", "", text)
    text = re.sub(r"''", "", text)
    text = re.sub(r"<ref.*?</ref>", "", text, flags=re.DOTALL)
    text = re.sub(r"<.*?>", "", text)

    # 6. Lọc dòng rác
    lines = text.split("\n")
    cleaned_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Bỏ qua dòng quá ngắn chỉ chứa ký tự đặc biệt
        if len(line) < 5 and not any(c.isalpha() for c in line):
            continue
            
        # Bỏ qua dòng bắt đầu bằng ký tự đặc biệt wiki
        if line.startswith("|") or line.startswith("{") or line.startswith("}"):
            continue
            
        # Bỏ qua dòng là URL trần
        if re.match(r"^https?://", line):
            continue

        cleaned_lines.append(line)
    
    text = "\n".join(cleaned_lines)

    # 7. Chuẩn hóa khoảng trắng
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r" {2,}", " ", text)
    text = re.sub(r"\t+", " ", text)

    # 8. Lọc đoạn văn ngắn vô nghĩa lần cuối
    paragraphs = text.split("\n\n")
    valid_paragraphs = []
    for para in paragraphs:
        para = para.strip()
        # Chỉ giữ đoạn đủ dài hoặc là tiêu đề (viết hoa, ngắn)
        if len(para) >= 40 or (len(para) > 5 and para.isupper()):
            valid_paragraphs.append(para)
    
    text = "\n\n".join(valid_paragraphs)

    return text.strip()
