-- ============================================================
-- SCRIPT TAO BANG CHO HE THONG GIAO TRINH AI
-- Database: giao_trinh_ai
-- ============================================================

USE giao_trinh_ai;

-- ============================================================
-- BANG 1: nguoi_dung (Người dùng)
-- ============================================================
CREATE TABLE IF NOT EXISTS nguoi_dung (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ten_dang_nhap VARCHAR(80) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    mat_khau_hash VARCHAR(255) NOT NULL,
    ho_ten VARCHAR(100),
    ngay_tao DATETIME DEFAULT CURRENT_TIMESTAMP,
    la_admin BOOLEAN DEFAULT FALSE,
    INDEX idx_ten_dang_nhap (ten_dang_nhap),
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- BANG 2: lich_su_giao_trinh (Lịch sử tạo giáo trình)
-- ============================================================
CREATE TABLE IF NOT EXISTS lich_su_giao_trinh (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nguoi_dung_id INT NOT NULL,
    chu_de VARCHAR(200) NOT NULL,
    noi_dung_html TEXT,
    duong_dan_file VARCHAR(500),
    do_dai_ky_tu INT DEFAULT 0,
    ngay_tao DATETIME DEFAULT CURRENT_TIMESTAMP,
    da_xuat_file BOOLEAN DEFAULT FALSE,
    INDEX idx_nguoi_dung_id (nguoi_dung_id),
    INDEX idx_ngay_tao (ngay_tao),
    FOREIGN KEY (nguoi_dung_id) 
        REFERENCES nguoi_dung(id) 
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- HOAN TAT
-- ============================================================
-- Sau khi chay script nay, ban se co 2 bang:
-- 1. nguoi_dung - Luu thong tin nguoi dung
-- 2. lich_su_giao_trinh - Luu lich su tao giao trinh
-- ============================================================
