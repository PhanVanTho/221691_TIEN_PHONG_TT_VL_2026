"""
Script migrate dữ liệu từ SQLite sang MySQL
"""
import os
import sqlite3
from dotenv import load_dotenv
import pymysql

def migrate_data():
    """Migrate dữ liệu từ SQLite sang MySQL"""
    
    print("=" * 60)
    print("🔄 MIGRATE DỮ LIỆU TỪ SQLITE SANG MYSQL")
    print("=" * 60)
    print()
    
    # Load .env
    load_dotenv()
    
    # Kiểm tra cấu hình MySQL
    db_type = os.getenv('DB_TYPE', 'sqlite')
    if db_type != 'mysql':
        print("❌ Chưa cấu hình MySQL trong file .env")
        print("💡 Chạy: python cau_hinh_mysql.py")
        return
    
    # Thông tin MySQL
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = int(os.getenv('DB_PORT', '3306'))
    db_user = os.getenv('DB_USER', 'root')
    db_password = os.getenv('DB_PASSWORD', '')
    db_name = os.getenv('DB_NAME', 'giao_trinh_ai')
    
    # Kiểm tra file SQLite
    sqlite_path = os.path.join(os.path.dirname(__file__), 'database.db')
    if not os.path.exists(sqlite_path):
        print("⚠️ Không tìm thấy file database.db")
        print("💡 Database sẽ được tạo mới khi chạy ứng dụng")
        return
    
    print(f"📂 Đang đọc dữ liệu từ: {sqlite_path}")
    
    try:
        # Kết nối SQLite
        sqlite_conn = sqlite3.connect(sqlite_path)
        sqlite_cursor = sqlite_conn.cursor()
        
        # Kết nối MySQL
        print(f"🔌 Đang kết nối MySQL: {db_host}:{db_port}/{db_name}")
        mysql_conn = pymysql.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
            database=db_name,
            charset='utf8mb4'
        )
        mysql_cursor = mysql_conn.cursor()
        
        # Migrate bảng nguoi_dung
        print("\n📊 Đang migrate bảng nguoi_dung...")
        sqlite_cursor.execute("SELECT * FROM nguoi_dung")
        users = sqlite_cursor.fetchall()
        
        if users:
            print(f"   Tìm thấy {len(users)} người dùng")
            for user in users:
                try:
                    mysql_cursor.execute("""
                        INSERT INTO nguoi_dung 
                        (id, ten_dang_nhap, email, mat_khau_hash, ho_ten, ngay_tao, la_admin)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                        ten_dang_nhap=VALUES(ten_dang_nhap),
                        email=VALUES(email),
                        mat_khau_hash=VALUES(mat_khau_hash),
                        ho_ten=VALUES(ho_ten)
                    """, user)
                    print(f"   ✅ Đã migrate: {user[1]}")
                except Exception as e:
                    print(f"   ⚠️ Lỗi với user {user[1]}: {str(e)}")
        else:
            print("   Không có dữ liệu người dùng")
        
        # Migrate bảng lich_su_giao_trinh
        print("\n📊 Đang migrate bảng lich_su_giao_trinh...")
        sqlite_cursor.execute("SELECT * FROM lich_su_giao_trinh")
        histories = sqlite_cursor.fetchall()
        
        if histories:
            print(f"   Tìm thấy {len(histories)} bản ghi lịch sử")
            for history in histories:
                try:
                    mysql_cursor.execute("""
                        INSERT INTO lich_su_giao_trinh
                        (id, nguoi_dung_id, chu_de, noi_dung_html, duong_dan_file, 
                         do_dai_ky_tu, ngay_tao, da_xuat_file)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                        chu_de=VALUES(chu_de),
                        noi_dung_html=VALUES(noi_dung_html),
                        duong_dan_file=VALUES(duong_dan_file)
                    """, history)
                except Exception as e:
                    print(f"   ⚠️ Lỗi với lịch sử ID {history[0]}: {str(e)}")
        else:
            print("   Không có dữ liệu lịch sử")
        
        # Commit
        mysql_conn.commit()
        
        # Đóng kết nối
        sqlite_conn.close()
        mysql_conn.close()
        
        print()
        print("=" * 60)
        print("✅ MIGRATE HOÀN TẤT!")
        print("=" * 60)
        print(f"   - Người dùng: {len(users)}")
        print(f"   - Lịch sử: {len(histories)}")
        print()
        
    except pymysql.Error as e:
        print(f"❌ Lỗi MySQL: {str(e)}")
        print("💡 Hãy đảm bảo:")
        print("   1. MySQL đã được cài đặt và chạy")
        print("   2. Database đã được tạo")
        print("   3. Thông tin kết nối trong .env đúng")
    except Exception as e:
        print(f"❌ Lỗi: {str(e)}")


if __name__ == "__main__":
    try:
        migrate_data()
    except KeyboardInterrupt:
        print("\n\n❌ Đã hủy bởi người dùng")
    except Exception as e:
        print(f"\n❌ Lỗi: {str(e)}")
