"""
Script kiểm tra và hướng dẫn xem database đúng
"""
import os
from dotenv import load_dotenv
import pymysql

def kiem_tra_database():
    """Kiểm tra database và hướng dẫn"""
    
    print("=" * 60)
    print("KIEM TRA DATABASE")
    print("=" * 60)
    print()
    
    # Load .env
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        load_dotenv(env_path)
        print("✅ Đã tìm thấy file .env")
    else:
        print("⚠️ Chưa có file .env")
        print("💡 Hãy tạo file .env với cấu hình MySQL")
        return
    
    db_type = os.getenv('DB_TYPE', 'sqlite')
    
    if db_type != 'mysql':
        print()
        print("⚠️ Hệ thống đang dùng SQLite (lưu trong máy)")
        print("💡 Để dùng MySQL, cập nhật .env với DB_TYPE=mysql")
        return
    
    # Thông tin MySQL
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = int(os.getenv('DB_PORT', '3306'))
    db_user = os.getenv('DB_USER', 'root')
    db_password = os.getenv('DB_PASSWORD', '')
    db_name = os.getenv('DB_NAME', 'giao_trinh_ai')
    
    print()
    print("Thông tin cấu hình MySQL:")
    print(f"  Host: {db_host}")
    print(f"  Port: {db_port}")
    print(f"  User: {db_user}")
    print(f"  Database: {db_name}")
    print()
    
    try:
        # Kết nối MySQL
        print("Đang kết nối MySQL...")
        conn = pymysql.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
            charset='utf8mb4'
        )
        cursor = conn.cursor()
        
        # Kiểm tra database có tồn tại không
        cursor.execute("SHOW DATABASES LIKE %s", (db_name,))
        db_exists = cursor.fetchone()
        
        if db_exists:
            print(f"✅ Database '{db_name}' đã tồn tại")
            
            # Kết nối vào database
            conn.select_db(db_name)
            
            # Kiểm tra các bảng
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            if tables:
                print(f"✅ Tìm thấy {len(tables)} bảng:")
                for table in tables:
                    table_name = table[0]
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                    count = cursor.fetchone()[0]
                    print(f"   - {table_name}: {count} bản ghi")
            else:
                print("⚠️ Chưa có bảng nào")
                print("💡 Chạy ứng dụng để tạo bảng tự động")
            
            # Hướng dẫn xem trong phpMyAdmin
            print()
            print("=" * 60)
            print("HUONG DAN XEM DU LIEU TRONG PHPMYADMIN")
            print("=" * 60)
            print()
            print(f"1. Mo phpMyAdmin: http://localhost:888/phpmyadmin/")
            print()
            print(f"2. Click vao database '{db_name}' o sidebar ben trai")
            print("   (KHONG phai database 'phpmyadmin')")
            print()
            print(f"3. URL dung se la:")
            print(f"   http://localhost:888/phpmyadmin/index.php?route=/database/structure&db={db_name}")
            print()
            print("4. Ban se thay cac bang:")
            print("   - nguoi_dung (du lieu nguoi dung)")
            print("   - lich_su_giao_trinh (lich su tao giao trinh)")
            print()
            
        else:
            print(f"❌ Database '{db_name}' CHUA duoc tao")
            print()
            print("=" * 60)
            print("HUONG DAN TAO DATABASE")
            print("=" * 60)
            print()
            print("1. Mo phpMyAdmin: http://localhost:888/phpmyadmin/")
            print()
            print("2. Click 'New' (Tao moi) o sidebar trai")
            print()
            print(f"3. Database name: {db_name}")
            print("   Collation: utf8mb4_unicode_ci")
            print()
            print("4. Click 'Create'")
            print()
            print("HOAC chay SQL:")
            print(f"   CREATE DATABASE {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
            print()
        
        conn.close()
        
    except pymysql.Error as e:
        print(f"❌ Loi ket noi MySQL: {str(e)}")
        print()
        print("Kiem tra:")
        print("  1. MySQL da chay trong XAMPP/WAMP chua?")
        print("  2. Thong tin trong .env co dung khong?")
        print("  3. Da cai pymysql chua? (pip install pymysql)")
    except Exception as e:
        print(f"❌ Loi: {str(e)}")


if __name__ == "__main__":
    try:
        kiem_tra_database()
    except KeyboardInterrupt:
        print("\n\n❌ Da huy boi nguoi dung")
    except Exception as e:
        print(f"\n❌ Loi: {str(e)}")
