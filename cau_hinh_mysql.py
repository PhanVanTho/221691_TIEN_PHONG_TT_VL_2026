"""
Script hỗ trợ cấu hình MySQL cho hệ thống giáo trình AI
"""
import os
from dotenv import load_dotenv

def cau_hinh_mysql():
    """Hướng dẫn và cấu hình MySQL"""
    
    print("=" * 60)
    print("🔧 CẤU HÌNH MYSQL CHO HỆ THỐNG GIÁO TRÌNH AI")
    print("=" * 60)
    print()
    
    # Kiểm tra file .env
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    
    if os.path.exists(env_path):
        load_dotenv(env_path)
        print("✅ Đã tìm thấy file .env")
    else:
        print("⚠️ Chưa có file .env, sẽ tạo mới")
    
    print()
    print("Vui lòng nhập thông tin MySQL của bạn:")
    print()
    
    # Nhập thông tin
    db_host = input("📍 MySQL Host [localhost]: ").strip() or "localhost"
    db_port = input("🔌 MySQL Port [3306]: ").strip() or "3306"
    db_user = input("👤 MySQL Username [root]: ").strip() or "root"
    db_password = input("🔐 MySQL Password: ").strip()
    db_name = input("📊 Database Name [giao_trinh_ai]: ").strip() or "giao_trinh_ai"
    
    print()
    print("=" * 60)
    print("📝 Thông tin đã nhập:")
    print(f"   Host: {db_host}")
    print(f"   Port: {db_port}")
    print(f"   User: {db_user}")
    print(f"   Database: {db_name}")
    print("=" * 60)
    print()
    
    xac_nhan = input("Xác nhận cấu hình? (y/n): ").strip().lower()
    
    if xac_nhan != 'y':
        print("❌ Đã hủy cấu hình")
        return
    
    # Đọc file .env hiện tại (nếu có)
    env_content = []
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            env_content = f.readlines()
    
    # Cập nhật hoặc thêm các dòng cấu hình
    config_lines = {
        'DB_TYPE': 'mysql',
        'DB_HOST': db_host,
        'DB_PORT': db_port,
        'DB_USER': db_user,
        'DB_PASSWORD': db_password,
        'DB_NAME': db_name
    }
    
    # Xử lý file .env
    existing_keys = set()
    new_lines = []
    
    for line in env_content:
        line_stripped = line.strip()
        if '=' in line_stripped and not line_stripped.startswith('#'):
            key = line_stripped.split('=')[0].strip()
            existing_keys.add(key)
            # Giữ lại các dòng không phải DB config
            if not key.startswith('DB_'):
                new_lines.append(line)
    
    # Thêm các cấu hình mới
    new_lines.append("\n# ===== MySQL Database Configuration =====\n")
    for key, value in config_lines.items():
        new_lines.append(f"{key}={value}\n")
    
    # Ghi file
    try:
        with open(env_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print()
        print("✅ Đã cập nhật file .env thành công!")
        print()
    except Exception as e:
        print(f"❌ Lỗi khi ghi file .env: {str(e)}")
        return
    
    # Hướng dẫn tiếp theo
    print("=" * 60)
    print("📋 CÁC BƯỚC TIẾP THEO:")
    print("=" * 60)
    print()
    print("1. Tạo database trong MySQL:")
    print(f"   CREATE DATABASE {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    print()
    print("2. Cài đặt driver MySQL:")
    print("   pip install pymysql cryptography")
    print()
    print("3. Chạy ứng dụng:")
    print("   python chay_he_thong.py")
    print()
    print("=" * 60)
    print("✅ Hoàn tất cấu hình!")
    print("=" * 60)


if __name__ == "__main__":
    try:
        cau_hinh_mysql()
    except KeyboardInterrupt:
        print("\n\n❌ Đã hủy bởi người dùng")
    except Exception as e:
        print(f"\n❌ Lỗi: {str(e)}")
