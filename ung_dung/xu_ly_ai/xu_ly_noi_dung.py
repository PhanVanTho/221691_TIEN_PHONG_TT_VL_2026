import re


def chia_doan(noi_dung: str, do_dai_toi_thieu=300, do_dai_toi_da=800):
    """
    Chia nội dung Wikipedia thành các đoạn có ý nghĩa một cách thông minh
    """
    if not noi_dung:
        return []
    
    # Tách theo đoạn văn (paragraph)
    paragraphs = noi_dung.split("\n\n")
    cac_doan = []
    buffer = ""

    for para in paragraphs:
        para = para.strip()
        if not para or len(para) < 20:
            continue

        # Nếu đoạn hiện tại đã đủ dài, thêm vào danh sách
        if len(buffer) >= do_dai_toi_thieu:
            cac_doan.append(buffer.strip())
            buffer = ""

        # Thêm đoạn mới vào buffer
        if buffer:
            buffer += " " + para
        else:
            buffer = para

        # Nếu buffer quá dài, cắt tại câu
        if len(buffer) > do_dai_toi_da:
            # Tìm vị trí cắt tại dấu chấm câu
            sentences = re.split(r'([.!?]\s+)', buffer)
            temp_buffer = ""
            
            for i in range(0, len(sentences), 2):
                if i + 1 < len(sentences):
                    sentence = sentences[i] + sentences[i + 1]
                else:
                    sentence = sentences[i]
                
                if len(temp_buffer + sentence) <= do_dai_toi_da:
                    temp_buffer += sentence
                else:
                    if temp_buffer:
                        cac_doan.append(temp_buffer.strip())
                    temp_buffer = sentence
            
            buffer = temp_buffer

    
    # Thêm phần còn lại
    if buffer and len(buffer) >= 50:
        cac_doan.append(buffer.strip())

    return cac_doan


def check_relevance(paragraph: str, topic: str) -> int:
    """
    Chấm điểm độ liên quan của đoạn văn với chủ đề.
    Return: Score (càng cao càng liên quan, < 0 là không liên quan)
    """
    if not paragraph or not topic:
        return 0
        
    para_lower = paragraph.lower()
    topic_words = topic.lower().split()
    
    score = 0
    
    # 1. Topic Appearance
    # Cộng điểm nếu tên chủ đề xuất hiện
    if topic.lower() in para_lower:
        score += 3
    # Cộng điểm nếu các từ trong chủ đề xuất hiện (partial match)
    elif any(w in para_lower for w in topic_words if len(w) > 2): 
        score += 1
        
    # 2. Context Keywords (Academic/Technical context)
    context_keywords = [
        "công nghệ", "hệ thống", "phương pháp", "nghiên cứu", "phát triển", 
        "khoa học", "kỹ thuật", "ứng dụng", "lý thuyết", "mô hình",
        "technology", "system", "method", "research", "development",
        "science", "technique", "application", "theory", "model"
    ]
    if any(k in para_lower for k in context_keywords):
        score += 0.5

    # 3. Penalty for "Meta" content (Wikipedia specifics)
    meta_keywords = [
        "xem thêm tại", "bài viết này", "liên kết ngoài", "tham khảo", 
        "chú thích", "dẫn nguồn", "bản mẫu", "thể loại",
        "see also", "external links", "references", "stub", "category"
    ]
    if any(k in para_lower for k in meta_keywords):
        score -= 2
        
    # 4. Penalty for short/navigational text
    if len(paragraph) < 100: 
        score -= 1
        
    return score


def loc_cac_doan_rac(cac_doan: list, topic: str = "") -> list:
    """
    Lọc bỏ các đoạn văn rác, không liên quan hoặc quá ngắn.
    """
    ket_qua = []
    seen_hashes = set()
    
    for doan in cac_doan:
        doan = doan.strip()
        
        # 1. Lọc theo độ dài
        if len(doan) < 60:
            continue
            
        # 2. Lọc trùng lặp (Dedup)
        h = hash(doan)
        if h in seen_hashes:
            continue
        seen_hashes.add(h)
        
        # 3. Lọc theo độ liên quan (nếu có topic)
        if topic:
            score = check_relevance(doan, topic)
            if score < 0: # Ngưỡng loại bỏ
                continue
                
        # 4. Lọc nội dung điều hướng Wiki cụ thể
        stop_phrases = [
            "^xem thêm", "^bài chính", "^tham khảo", "^liên kết", 
            "^chú thích", "^nguồn", "^đọc thêm", "^thể loại",
            "bạn có thể giúp wikipedia", "bài viết này cần",
            "This article", "See also", "References", "External links"
        ]
        if any(re.search(p, doan, re.IGNORECASE) for p in stop_phrases):
             continue

        ket_qua.append(doan)
            
    return ket_qua



def phan_loai_noi_dung(cac_doan: list, chu_de: str = "") -> dict:
    """
    Phân loại các đoạn văn thành các loại: giới thiệu, khái niệm, lịch sử, ứng dụng, v.v.
    Hỗ trợ cả tiếng Việt và tiếng Anh.
    Sử dụng 'chu_de' để tăng độ chính xác khi phân loại.
    """
    if not cac_doan:
        return {
            "gioi_thieu": [],
            "khai_niem": [],
            "lich_su": [],
            "ung_dung": [],
            "phuong_phap": [],
            "tuong_lai": [],
            "dao_duc": [],
            "khac": []
        }
    
    # Từ khóa Tiếng Việt + Tiếng Anh
    tu_khoa_gioi_thieu = [
        "là", "được định nghĩa", "là một", "là loại", "là hệ thống", 
        "is a", "is the", "refers to", "defined as", "introduction", "overview"
    ]
    tu_khoa_khai_niem = [
        "khái niệm", "định nghĩa", "đặc điểm", "thành phần", "nguyên lý", "cấu trúc",
        "concept", "definition", "feature", "characteristic", "principle", "structure", "component"
    ]
    tu_khoa_lich_su = [
        "lịch sử", "phát triển", "ra đời", "năm", "thế kỷ", "thập niên", "nguồn gốc",
        "history", "development", "year", "century", "originated", "founded", "origin"
    ]
    tu_khoa_ung_dung = [
        "ứng dụng", "sử dụng", "áp dụng", "trong", "ví dụ", "case study",
        "application", "usage", "used in", "example", "case study", "applied", "use case"
    ]
    tu_khoa_phuong_phap = [
        "phương pháp", "kỹ thuật", "cách thức", "thuật toán", "quy trình", "công nghệ",
        "method", "technique", "algorithm", "process", "approach", "technology"
    ]
    tu_khoa_tuong_lai = [
        "tương lai", "xu hướng", "dự đoán", "triển vọng", "tiềm năng",
        "future", "trend", "prediction", "prospect", "potential"
    ]
    tu_khoa_dao_duc = [
        "đạo đức", "pháp luật", "rủi ro", "an toàn", "trách nhiệm", "xã hội", "tác động",
        "ethics", "law", "legal", "risk", "safety", "responsibility", "social", "impact", "bias"
    ]
    
    
    phan_loai = {
        "gioi_thieu": [],
        "khai_niem": [],
        "lich_su": [],
        "ung_dung": [],
        "phuong_phap": [],
        "tuong_lai": [],
        "dao_duc": [],
        "khac": []
    }
    
    # Pre-process: Lọc rác trước khi phân loại (nếu chưa lọc)
    # Tuy nhiên, hàm này thường được gọi sau khi đã có danh sách sạch, 
    # nên ta giả định input 'cac_doan' đã tương đối sạch.
    
    for doan in cac_doan:
        doan_lower = doan.lower()
        da_phan_loai = False
        
        # Helper: Check keyword with rigorous matching
        def has_keywords(text, keywords):
            return any(k in text for k in keywords)

        # 1. GIỚI THIỆU: Định nghĩa trực tiếp (X là Y)
        # Yêu cầu: Phải có tên chủ đề HOẶC là đoạn đầu tiên (được xử lý ở nơi gọi hàm)
        is_definition = any(k in doan_lower for k in tu_khoa_gioi_thieu)
        if is_definition and len(phan_loai["gioi_thieu"]) < 3: 
             # Ưu tiên nếu đoạn văn chứa chủ đề
             if (not chu_de) or (chu_de.lower() in doan_lower):
                phan_loai["gioi_thieu"].append(doan)
                da_phan_loai = True

        # 2. LỊCH SỬ: Thời gian + Từ khóa lịch sử
        # Yêu cầu: Phải có từ khóa lịch sử VÀ (năm HOẶC từ chỉ thời gian)
        if not da_phan_loai and has_keywords(doan_lower, tu_khoa_lich_su):
             time_markers = ["năm", "thế kỷ", "thập niên", "year", "century", "decade", "19", "20"]
             if any(tm in doan_lower for tm in time_markers):
                phan_loai["lich_su"].append(doan)
                da_phan_loai = True

        # 3. ĐẠO ĐỨC / XÃ HỘI
        if not da_phan_loai and has_keywords(doan_lower, tu_khoa_dao_duc):
            phan_loai["dao_duc"].append(doan)
            da_phan_loai = True

        # 4. TƯƠNG LAI / XU HƯỚNG
        if not da_phan_loai and has_keywords(doan_lower, tu_khoa_tuong_lai):
            phan_loai["tuong_lai"].append(doan)
            da_phan_loai = True

        # 5. PHƯƠNG PHÁP / KỸ THUẬT
        if not da_phan_loai and has_keywords(doan_lower, tu_khoa_phuong_phap):
            phan_loai["phuong_phap"].append(doan)
            da_phan_loai = True

        # 6. ỨNG DỤNG: Cần ngữ cảnh cụ thể
        if not da_phan_loai and has_keywords(doan_lower, tu_khoa_ung_dung):
             # Tránh các đoạn chung chung kiểu "thuật ngữ này được sử dụng..."
             if len(doan) > 150: # Đoạn dài thường tin cậy hơn
                phan_loai["ung_dung"].append(doan)
                da_phan_loai = True

        # 7. KHÁI NIỆM / CẤU TRÚC
        if not da_phan_loai and has_keywords(doan_lower, tu_khoa_khai_niem):
            phan_loai["khai_niem"].append(doan)
            da_phan_loai = True
        
        # Mặc định: Nếu không khớp loại nào
        if not da_phan_loai:
            # Check kỹ hơn để vớt vát vào Khái niệm hoặc Ứng dụng nếu đoạn văn chất lượng cao
            if len(doan) > 200:
                 phan_loai["khac"].append(doan)
            # Đoạn quá ngắn không phân loại được coi như bỏ qua hoặc cho vào 'khac' nếu cần thiết
            # Ở đây ta vẫn giữ lại để không mất nội dung, nhưng xếp vào 'khac'
            else:
                 phan_loai["khac"].append(doan)
    
    return phan_loai

def trich_xuat_vi_du(cac_doan: list) -> list:
    """
    Trích xuất các đoạn văn chứa ví dụ (cho trường hợp muốn lọc từ nội dung chính)
    """
    tu_khoa_vi_du = [
        "ví dụ", "chẳng hạn", "case study", "thực tiễn", "minh họa",
        "example", "instance", "such as", "illustration", "namely"
    ]
    
    vi_du_list = []
    for doan in cac_doan:
        if any(tk in doan.lower() for tk in tu_khoa_vi_du):
            vi_du_list.append(doan)
            
    return vi_du_list


    return vi_du_list


def tim_tu_khoa_pho_bien(text: str, top_n=1) -> str:
    """
    Tìm từ khóa/cụm từ xuất hiện nhiều nhất trong văn bản.
    Hỗ trợ n-grams (1-3 từ).
    """
    if not text:
        return ""
        
    # 1. Tokenize & Clean
    text_clean = re.sub(r"[^\w\s]", " ", text.lower())
    words = [w for w in text_clean.split() if len(w) > 1 and not w.isnumeric()]
    
    # Stopwords tiếng Việt cơ bản
    stopwords = {
        "là", "của", "và", "các", "những", "trong", "được", "với", "cho", 
        "người", "khi", "có", "này", "đó", "tại", "về", "như", "nhưng",
        "từ", "lại", "ra", "đã", "đang", "sẽ", "để", "cũng", "một", "nhiều",
        "hơn", "rất", "thì", "mà", "theo", "bởi", "vì", "nên", "do", "tuy",
        "chúng", "tôi", "anh", "chị", "ông", "bà", "nó", "chúng_ta", "họ",
        # English Stopwords
        "the", "be", "to", "of", "and", "a", "in", "that", "have", "i",
        "it", "for", "not", "on", "with", "he", "as", "you", "do", "at",
        "this", "but", "his", "by", "from", "they", "we", "say", "her",
        "she", "or", "an", "will", "my", "one", "all", "would", "there",
        "their", "what", "so", "up", "out", "if", "about", "who", "get",
        "which", "go", "me", "when", "make", "can", "like", "time", "no",
        "just", "him", "know", "take", "person", "into", "year", "your",
        "good", "some", "could", "them", "see", "other", "than", "then",
        "now", "look", "only", "come", "its", "over", "think", "also",
        "back", "after", "use", "two", "how", "our", "work", "first",
        "well", "way", "even", "new", "want", "because", "any", "these",
        "give", "day", "most", "us", "is", "are", "was", "were", "has"
    }
    
    words = [w for w in words if w not in stopwords]
    
    if not words:
        return ""

    # 2. Count frequencies (Unigrams, Bigrams, Trigrams)
    freq_dist = {}
    
    # Helper to count n-grams
    def add_ngrams(n):
        for i in range(len(words) - n + 1):
            gram = " ".join(words[i:i+n])
            freq_dist[gram] = freq_dist.get(gram, 0) + (n * 1.5) # Ưu tiên cụm từ dài hơn
            
    add_ngrams(1)
    add_ngrams(2)
    add_ngrams(3)
    
    # 3. Find max
    # Lọc những từ chỉ xuất hiện 1 lần nếu văn bản dài
    min_tf = 2 if len(words) > 30 else 1
    
    candidates = sorted(freq_dist.items(), key=lambda x: x[1], reverse=True)
    
    for word, score in candidates:
        # Nếu score cao và không phải là stopword (check lại cho cụm từ)
        if score >= min_tf:
             # Heuristic: Cụm từ 2-3 từ thường là thuật ngữ tốt
             return word.title()
             
    return ""


def tao_tieu_de_doan(noi_dung_doan: str, chu_de_chinh: str = "") -> str:
    """
    Tạo tiêu đề ngắn gọn (khoảng 3-8 từ) dựa trên nội dung đoạn văn.
    Kết hợp Heuristics và Keyword Extraction.
    """
    if not noi_dung_doan:
        return "Nội dung chi tiết"
        
    # 1. Tiền xử lý: Làm sạch cơ bản
    noi_dung_doan = re.sub(r'\s+', ' ', noi_dung_doan.strip())
    
    # Lấy câu đầu tiên để phân tích
    sentences = re.split(r'(?<=[.!?])\s+', noi_dung_doan)
    cau_dau = sentences[0].strip() if sentences else noi_dung_doan
    cau_dau_lower = cau_dau.lower()
    
    # 2. Heuristic Level 1: Cấu trúc Định nghĩa ("X là Y", "X được gọi là Y")
    match_def = re.search(r'^(.+?)\s+(?:là|được\s+(?:xem|gọi|định\s+nghĩa|coi)\s+là)', cau_dau, re.IGNORECASE)
    if match_def:
        subject = match_def.group(1).strip()
        if len(subject.split()) <= 10:
            # Nếu Subject quá giống Topic chính -> "Khái niệm..."
            if chu_de_chinh and chu_de_chinh.lower() in subject.lower():
                return "Khái niệm và định nghĩa"
            # Cleanup subject
            subject = re.sub(r'^(việc|sự|quá trình)\s+', '', subject, flags=re.IGNORECASE)
            return subject[0].upper() + subject[1:]

    # 3. Heuristic Level 2: Các từ khóa chỉ dẫn (Indicator Keywords)
    if re.match(r'^(?:được\s+)?sử\s+dụng\s+(?:để|trong|cho)', cau_dau_lower): return "Ứng dụng và mục đích sử dụng"
    if re.match(r'^giúp\s+', cau_dau_lower): return "Lợi ích và vai trò"
    if any(k in cau_dau_lower for k in ["năm", "thế kỷ", "thập niên"]):
        nam = re.search(r'\b(19|20)\d{2}\b', cau_dau)
        return f"Dấu mốc lịch sử năm {nam.group(0)}" if nam else "Bối cảnh lịch sử"
    if any(k in cau_dau_lower for k in ["bao gồm", "chia thành", "phân thành", "gồm có"]): return "Phân loại và thành phần"
    if "ưu điểm" in cau_dau_lower: return "Ưu điểm nổi bật"
    if "nhược điểm" in cau_dau_lower or "hạn chế" in cau_dau_lower: return "Hạn chế và thách thức"

    # [NEW] English Heuristics
    # Definition
    if any(p in cau_dau_lower for p in ["is defined as", "refers to", "can be described", "is a type of"]):
        return "Concept and Definition"
    # Usage/Application
    if any(p in cau_dau_lower for p in ["used for", "used in", "applied in", "application of", "serves to"]):
         return "Applications and Usage"
    # History
    if any(p in cau_dau_lower for p in ["history of", "originated in", "first developed", "founded in"]):
         return "Historical Background"
    # Components
    if any(p in cau_dau_lower for p in ["consists of", "composed of", "includes", "contains", "divided into"]):
         return "Components and Structure"
    # Pros/Cons
    if any(p in cau_dau_lower for p in ["advantage", "benefit", "strength"]): return "Key Advantages"
    if any(p in cau_dau_lower for p in ["disadvantage", "limitation", "weakness", "monitor"]): return "Limitations and Challenges"

    # 4. Keyword Extraction (NEW: Smart Logic)
    # Nếu các rule trên không bắt được, ta thử tìm từ khóa lặp lại nhiều nhất trong cả đoạn
    # Điều này giúp bắt được chủ đề của đoạn văn mô tả sâu về một khái niệm con
    keyword_title = tim_tu_khoa_pho_bien(noi_dung_doan)
    if keyword_title and len(keyword_title) > 3: # Đảm bảo từ khóa có nghĩa
        if chu_de_chinh and keyword_title.lower() in chu_de_chinh.lower():
             pass # Nếu keyword tr trùng topic chính -> Fallback xuống dưới để lấy text tự nhiên hơn
        else:
             # Tiếng Việt
             if re.search(r'[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]', noi_dung_doan):
                 return f"Tìm hiểu về {keyword_title}"
             else:
                 # [NEW] English Smart Titles
                 import random
                 templates = [
                     f"Understanding {keyword_title}",
                     f"The Role of {keyword_title}",
                     f"Key Aspects of {keyword_title}",
                     f"Overview of {keyword_title}",
                     f"Introduction to {keyword_title}"
                 ]
                 return random.choice(templates)

    # 5. Fallback Level 3: Rút gọn câu đầu (Logic cũ nhưng tối ưu lại)
    # Xóa từ nối đầu câu
    tu_khoa_loai_bo = ["tuy nhiên", "mặc dù", "hơn nữa", "ngoài ra", "mặt khác", "trong khi đó", "thực tế", "bởi vì", "do đó", "vì vậy"]
    processed_cau_dau = cau_dau
    for tu in tu_khoa_loai_bo:
         if processed_cau_dau.lower().startswith(tu):
             processed_cau_dau = re.sub(f"^{tu}[:,\\s]*", "", processed_cau_dau, flags=re.IGNORECASE).strip()
             break
             
    words = processed_cau_dau.split()
    if len(words) < 3: return processed_cau_dau
    
    # Cắt ở dấu phẩy hợp lý
    first_comma = processed_cau_dau.find(',')
    if 15 < first_comma < 60:
         return processed_cau_dau[:first_comma].strip()

    return " ".join(words[:7]).strip() + ("..." if len(words) > 7 else "")
