"""
Script cấu hình MySQL cho phpMyAdmin tại localhost:888
"""
import os
import sys

# Fix encoding cho Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def cau_hinh_phpmyadmin():
    """Cấu hình MySQL cho phpMyAdmin"""
    
    print("=" * 60)
    print("🔧 CẤU HÌNH MYSQL CHO PHPMYADMIN")
    print("=" * 60)
    print()
    print("📍 phpMyAdmin URL: http://localhost:888/phpmyadmin/")
    print()
    
    # Thông tin mặc định cho XAMPP/WAMP
    print("Thông tin mặc định cho XAMPP/WAMP:")
    print("  - Host: localhost")
    print("  - Port: 3306")
    print("  - Username: root")
    print("  - Password: (thường để trống)")
    print()
    
    # Nhập thông tin
    db_host = input("📍 MySQL Host [localhost]: ").strip() or "localhost"
    db_port = input("🔌 MySQL Port [3306]: ").strip() or "3306"
    db_user = input("👤 MySQL Username [root]: ").strip() or "root"
    db_password = input("🔐 MySQL Password (Enter nếu không có): ").strip()
    db_name = input("📊 Database Name [giao_trinh_ai]: ").strip() or "giao_trinh_ai"
    
    print()
    print("=" * 60)
    print("📝 Thông tin đã nhập:")
    print(f"   Host: {db_host}")
    print(f"   Port: {db_port}")
    print(f"   User: {db_user}")
    print(f"   Password: {'***' if db_password else '(không có)'}")
    print(f"   Database: {db_name}")
    print("=" * 60)
    print()
    
    xac_nhan = input("Xác nhận cấu hình? (y/n): ").strip().lower()
    
    if xac_nhan != 'y':
        print("❌ Đã hủy cấu hình")
        return
    
    # Đường dẫn file .env
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    
    # Đọc file .env hiện tại (nếu có)
    env_content = []
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            env_content = f.readlines()
    
    # Xử lý file .env
    new_lines = []
    db_config_added = False
    
    for line in env_content:
        line_stripped = line.strip()
        # Giữ lại các dòng không phải DB config
        if not line_stripped.startswith('DB_'):
            new_lines.append(line)
        elif line_stripped.startswith('DB_TYPE'):
            # Cập nhật DB_TYPE
            new_lines.append(f"DB_TYPE=mysql\n")
            db_config_added = True
    
    # Thêm các cấu hình MySQL nếu chưa có
    if not db_config_added:
        new_lines.append("\n# ===== MySQL Database Configuration =====\n")
        new_lines.append("DB_TYPE=mysql\n")
    
    new_lines.append(f"DB_HOST={db_host}\n")
    new_lines.append(f"DB_PORT={db_port}\n")
    new_lines.append(f"DB_USER={db_user}\n")
    new_lines.append(f"DB_PASSWORD={db_password}\n")
    new_lines.append(f"DB_NAME={db_name}\n")
    
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
    print("1. Mở phpMyAdmin: http://localhost:888/phpmyadmin/")
    print()
    print("2. Tạo database (nếu chưa có):")
    print(f"   - Click 'New' (Tạo mới) ở sidebar trái")
    print(f"   - Database name: {db_name}")
    print(f"   - Collation: utf8mb4_unicode_ci")
    print(f"   - Click 'Create'")
    print()
    print("3. Cài đặt driver MySQL:")
    print("   pip install pymysql cryptography")
    print()
    print("4. Chạy ứng dụng:")
    print("   python chay_he_thong.py")
    print()
    print("=" * 60)
    print("✅ Hoàn tất cấu hình!")
    print("=" * 60)
    print()
    print("💡 Lưu ý:")
    print("   - Đảm bảo MySQL service đang chạy trong XAMPP/WAMP")
    print("   - Nếu password để trống, để trống DB_PASSWORD trong .env")
    print()


if __name__ == "__main__":
    try:
        cau_hinh_phpmyadmin()
    except KeyboardInterrupt:
        print("\n\n❌ Đã hủy bởi người dùng")
    except Exception as e:
        print(f"\n❌ Lỗi: {str(e)}")
