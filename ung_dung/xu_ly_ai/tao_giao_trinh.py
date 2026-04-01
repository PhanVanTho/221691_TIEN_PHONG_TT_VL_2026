from ung_dung.xu_ly_ai.wikipedia import lay_noi_dung_wikipedia
from ung_dung.xu_ly_ai.xu_ly_noi_dung import chia_doan, phan_loai_noi_dung, tao_tieu_de_doan, loc_cac_doan_rac
from ung_dung.thu_thap_du_lieu.lam_sach_van_ban import lam_sach_van_ban
from ung_dung.xu_ly_ai.dich_thuat import dich_danh_sach_doan, dich_sang_tieng_viet


def tao_giao_trinh(chu_de: str):
    """
    Tạo giáo trình với bố cục nâng cấp, phân loại nội dung thông minh,
    tích hợp hình ảnh và các ví dụ thực tế.
    """
    # [NEW] Dịch chủ đề sang Tiếng Việt ngay từ đầu để dùng cho hiển thị
    print(f"Dang dich chu de '{chu_de}' sang Tieng Viet...")
    chu_de_vi = dich_sang_tieng_viet(chu_de)
    
    # 1. Lấy dữ liệu đa phương tiện từ Wikipedia
    du_lieu_wiki = lay_noi_dung_wikipedia(chu_de) or {}
    
    # Check return type (handle legacy str return just in case, though we updated it)
    if isinstance(du_lieu_wiki, dict):
        noi_dung_tho = du_lieu_wiki.get("text", "")
        images = du_lieu_wiki.get("images", [])
        examples_content = du_lieu_wiki.get("examples", "")
    else:
        noi_dung_tho = str(du_lieu_wiki)
        images = []
        examples_content = ""

    if not noi_dung_tho or len(noi_dung_tho) < 500:
        return {
            "noi_dung": f"<div class='error-message'><p><b>⚠ Không tìm được nội dung phù hợp cho chủ đề '{chu_de_vi}'.</b></p><p>Vui lòng thử với chủ đề khác hoặc kiểm tra kết nối mạng.</p></div>"
        }

    # 2. Làm sạch Wiki markup
    noi_dung_sach = lam_sach_van_ban(noi_dung_tho)

    # 3. Chia đoạn thông minh
    cac_doan = chia_doan(noi_dung_sach)
    
    # [NEW] Dịch thuật: Dịch danh sách các đoạn văn sang Tiếng Việt
    # Việc dịch ở đây giúp đảm bảo toàn bộ nội dung sau này (phân loại, hiển thị) đều là TV.
    print(f"Dang dich {len(cac_doan)} doan van sang Tieng Viet...")
    cac_doan = dich_danh_sach_doan(cac_doan)
    
    # Kiểm tra nếu không có đủ đoạn
    if not cac_doan or len(cac_doan) < 3:
        return {
            "noi_dung": "<div class='error-message'><p><b>⚠ Nội dung quá ngắn, không đủ để tạo giáo trình cho '{chu_de_vi}'.</b></p></div>"
        }

    # 4. Lọc nội dung rác & Phân loại nội dung thông minh
    cac_doan_sach = loc_cac_doan_rac(cac_doan, topic=chu_de_vi)
    phan_loai = phan_loai_noi_dung(cac_doan_sach, chu_de=chu_de_vi)
    
    # Update lại danh sách chính sau khi lọc để fallback nếu cần
    if cac_doan_sach:
        cac_doan = cac_doan_sach
    
    # Xử lý Examples riêng
    examples_paragraphs = []
    if examples_content:
        examples_clean = lam_sach_van_ban(examples_content)
        examples_paragraphs = chia_doan(examples_clean)
        # [NEW] Dịch examples
        print(f"Dang dich {len(examples_paragraphs)} doan vi du sang Tieng Viet...")
        examples_paragraphs = dich_danh_sach_doan(examples_paragraphs)
    
    # Lấy các đoạn đã phân loại
    gioi_thieu = phan_loai["gioi_thieu"] or cac_doan[0:1]
    khai_niem = phan_loai["khai_niem"] or cac_doan[1:3] if len(cac_doan) >= 3 else cac_doan[1:2]
    lich_su = phan_loai["lich_su"] or []
    ung_dung = phan_loai["ung_dung"] or cac_doan[3:5] if len(cac_doan) >= 5 else cac_doan[2:4] if len(cac_doan) >= 4 else []
    
    # 5. Helper function tạo thẻ ảnh
    def tao_anh_html(index):
        if index < len(images):
            return f'<div class="image-container"><img src="{images[index]}" alt="Hình minh họa {index+1}" class="content-image"></div>'
        return ""

    # 6. Tạo HTML với bố cục đẹp hơn - REFACTORED for TOC
    toc_html = ""
    chapters_html = ""
    chapter_count = 0
    
    # --- CHƯƠNG 1: TỔNG QUAN ---
    chapter_count += 1
    toc_html += f'<li class="toc-item"><a href="#chuong-{chapter_count}">Chương {chapter_count}: Tổng quan về {chu_de_vi}</a></li>'
    
    chapters_html += f"""
            <div class="chuong" id="chuong-{chapter_count}">
                <h3 class="chuong-title">Chương {chapter_count}: Tổng quan về {chu_de_vi}</h3>
                <div class="chuong-content">
                    {tao_anh_html(0)}
                    {''.join(f'<p class="paragraph">{doan}</p>' for doan in gioi_thieu)}
                </div>
            </div>
    """
    
    # --- CÁC CHƯƠNG TIẾP THEO (LOOP) ---
    # Danh sách các mục tiềm năng để tạo chương
    # Tuple format: (key_in_phan_loai, Title, Icon_Index_Image)
    cac_chuong_tiem_nang = [
        ("khai_niem", "Khái niệm và nền tảng cốt lõi", 1),
        ("lich_su", "Lịch sử phát triển và nguồn gốc", None),
        ("phuong_phap", "Phương pháp, Kỹ thuật và Công nghệ", None),
        ("ung_dung", "Ứng dụng thực tiễn và Case Studies", 2),
        ("tuong_lai", "Xu hướng tương lai và Tiềm năng", None),
        ("dao_duc", "Vấn đề Đạo đức, Pháp luật và Xã hội", None),
        ("khac", "Các chủ đề mở rộng khác", None)
    ]
    
    for key, title, img_idx in cac_chuong_tiem_nang:
        content_list = phan_loai.get(key, [])
        if content_list:
            chapter_count += 1
            toc_html += f'<li class="toc-item"><a href="#chuong-{chapter_count}">Chương {chapter_count}: {title}</a></li>'
            
            # Chọn ảnh cho chương nếu có
            img_html = ""
            if img_idx is not None:
                img_html = tao_anh_html(img_idx) 
            elif chapter_count % 3 == 0: # Random ảnh cho các chương khác nếu chưa dùng
                 img_html = tao_anh_html(3 + (chapter_count // 3))
            
            # Tạo nội dung chương
            chapter_content = ""
            for i, doan in enumerate(content_list):
                 sub_title = tao_tieu_de_doan(doan, chu_de_vi)
                 chapter_content += f'<div class="sub-section"><h4 class="sub-title">{chapter_count}.{i+1} {sub_title}</h4><p class="paragraph">{doan}</p></div>'
            
            chapters_html += f"""
            <div class="chuong" id="chuong-{chapter_count}">
                <h3 class="chuong-title">Chương {chapter_count}: {title}</h3>
                <div class="chuong-content">
                    {img_html}
                    {chapter_content}
                </div>
            </div>
            """

    # --- CHƯƠNG VÍ DỤ ---
    if examples_paragraphs:
        chapter_count += 1
        toc_html += f'<li class="toc-item"><a href="#chuong-{chapter_count}">Chương {chapter_count}: Phân tích ví dụ chuyên sâu</a></li>'
        chapters_html += f"""
        <div class="chuong" id="chuong-{chapter_count}">
            <h3 class="chuong-title">Chương {chapter_count}: Phân tích ví dụ chuyên sâu</h3>
            <div class="chuong-content">
                {tao_anh_html(3)}
                {''.join(f'<div class="example-box"><p><strong><i class="fas fa-lightbulb"></i> Ví dụ {i+1}:</strong> {doan}</p></div>' for i, doan in enumerate(examples_paragraphs))}
            </div>
        </div>
        """

    # --- CHƯƠNG THỰC HÀNH & ĐÁNH GIÁ ---
    idx_chap_practice = chapter_count + 1
    idx_chap_eval = chapter_count + 2
    toc_html += f'<li class="toc-item"><a href="#chuong-{idx_chap_practice}">Chương {idx_chap_practice}: Thực hành và bài tập</a></li>'
    toc_html += f'<li class="toc-item"><a href="#chuong-{idx_chap_eval}">Chương {idx_chap_eval}: Kiểm tra và đánh giá</a></li>'

    chapters_html += f"""
            <div class="chuong" id="chuong-{idx_chap_practice}">
                <h3 class="chuong-title">Chương {idx_chap_practice}: Thực hành và bài tập</h3>
                <div class="chuong-content">
                    <div class="practice-list">
                        <div class="practice-item"><i class="fas fa-pencil-alt"></i> Phân tích các ví dụ thực tế về {chu_de_vi}</div>
                        <div class="practice-item"><i class="fas fa-laptop-code"></i> Liên hệ và ứng dụng trong lĩnh vực CNTT</div>
                        <div class="practice-item"><i class="fas fa-users"></i> Nghiên cứu case study và bài tập nhóm</div>
                    </div>
                </div>
            </div>

            <div class="chuong" id="chuong-{idx_chap_eval}">
                <h3 class="chuong-title">Chương {idx_chap_eval}: Kiểm tra và đánh giá</h3>
                <div class="chuong-content">
                    <div class="evaluation-grid">
                        <div class="eval-item">
                            <strong><i class="fas fa-check-square"></i> Hình thức 1:</strong> Câu hỏi trắc nghiệm (30%)
                        </div>
                        <div class="eval-item">
                            <strong><i class="fas fa-pen-fancy"></i> Hình thức 2:</strong> Câu hỏi tự luận (40%)
                        </div>
                        <div class="eval-item">
                            <strong><i class="fas fa-project-diagram"></i> Hình thức 3:</strong> Bài tập thực hành (30%)
                        </div>
                    </div>
                </div>
            </div>
    """

    # --- ASSEMBLE FINAL HTML ---
    html = f"""
    <div class="giao-trinh-container">
        <header class="giao-trinh-header">
            <h1 class="main-title"><i class="fas fa-book-open"></i> GIÁO TRÌNH: {chu_de_vi.upper()}</h1>
            <div class="meta-info">
                <span class="meta-item"><i class="far fa-calendar-alt"></i> Ngày tạo: {__import__('datetime').datetime.now().strftime('%d/%m/%Y')}</span>
                <span class="meta-item"><i class="fas fa-graduation-cap"></i> Số tín chỉ: 3</span>
            </div>
        </header>

        <section class="thong-tin-hoc-phan">
            <h2 class="section-title"><i class="fas fa-info-circle"></i> 1. Thông tin học phần</h2>
            <div class="info-grid">
                <div class="info-item">
                    <strong>Tên học phần:</strong> {chu_de_vi}
                </div>
                <div class="info-item">
                    <strong>Số tín chỉ:</strong> 3
                </div>
                <div class="info-item">
                    <strong>Đối tượng:</strong> Sinh viên CNTT
                </div>
                <div class="info-item">
                    <strong>Hình thức học:</strong> Lý thuyết + Thực hành
                </div>
            </div>
        </section>

        <section class="muc-tieu">
            <h2 class="section-title"><i class="fas fa-bullseye"></i> 2. Mục tiêu học phần (CLO)</h2>
            <div class="clo-list">
                <div class="clo-item">
                    <span class="clo-number">CLO1</span>
                    <span class="clo-content">Hiểu và nắm vững các khái niệm cơ bản và nền tảng về {chu_de_vi}</span>
                </div>
                <div class="clo-item">
                    <span class="clo-number">CLO2</span>
                    <span class="clo-content">Phân tích và đánh giá các ứng dụng thực tiễn của {chu_de_vi}</span>
                </div>
                <div class="clo-item">
                    <span class="clo-number">CLO3</span>
                    <span class="clo-content">Vận dụng kiến thức để giải quyết các vấn đề thực tế</span>
                </div>
            </div>
        </section>

        <section class="noi-dung-hoc-phan">
            <h2 class="section-title"><i class="fas fa-list-alt"></i> 3. Nội dung học phần</h2>
            
            <div class="muc-luc">
                <h4 style="margin-top: 0; color: var(--primary-dark);"><i class="fas fa-list-ol"></i> Mục lục</h4>
                <ul class="toc-list">
                    {toc_html}
                </ul>
            </div>

            {chapters_html}
        </section>

        <section class="tai-lieu-tham-khao">
            <h2 class="section-title"><i class="fas fa-book"></i> 4. Tài liệu tham khảo</h2>
            <div class="reference-list">
                <div class="ref-item"><i class="fab fa-wikipedia-w"></i> Wikipedia tiếng Việt/Anh - {chu_de}</div>
                <div class="ref-item"><i class="fas fa-book"></i> Giáo trình chuyên ngành CNTT</div>
                <div class="ref-item"><i class="fas fa-globe"></i> Tài liệu trực tuyến và bài báo khoa học</div>
            </div>
        </section>
    </div>
    """

    return {
        "noi_dung": html,
        "chu_de_vi": chu_de_vi
    }
