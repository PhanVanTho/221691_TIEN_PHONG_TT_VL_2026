"""
Script kiểm tra dữ liệu trong MySQL
"""
import os
from dotenv import load_dotenv
import pymysql

def kiem_tra_du_lieu():
    """Kiểm tra dữ liệu trong database"""
    
    print("=" * 60)
    print("KIEM TRA DU LIEU TRONG MYSQL")
    print("=" * 60)
    print()
    
    # Load .env
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if not os.path.exists(env_path):
        print("❌ Khong tim thay file .env")
        return
    
    load_dotenv(env_path)
    
    db_type = os.getenv('DB_TYPE', 'sqlite')
    if db_type != 'mysql':
        print("⚠️ He thong dang dung SQLite, khong phai MySQL")
        return
    
    # Thông tin MySQL
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = int(os.getenv('DB_PORT', '3306'))
    db_user = os.getenv('DB_USER', 'root')
    db_password = os.getenv('DB_PASSWORD', '')
    db_name = os.getenv('DB_NAME', 'giao_trinh_ai')
    
    try:
        # Kết nối MySQL
        print("Dang ket noi MySQL...")
        conn = pymysql.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
            database=db_name,
            charset='utf8mb4'
        )
        cursor = conn.cursor()
        
        print(f"✅ Ket noi thanh cong: {db_name}")
        print()
        
        # Kiểm tra bảng nguoi_dung
        print("=" * 60)
        print("BANG: nguoi_dung")
        print("=" * 60)
        
        cursor.execute("SELECT COUNT(*) FROM nguoi_dung")
        count = cursor.fetchone()[0]
        print(f"So luong nguoi dung: {count}")
        print()
        
        if count > 0:
            cursor.execute("""
                SELECT id, ten_dang_nhap, email, ho_ten, ngay_tao, la_admin 
                FROM nguoi_dung 
                ORDER BY ngay_tao DESC
            """)
            users = cursor.fetchall()
            
            print("Danh sach nguoi dung:")
            print("-" * 60)
            for user in users:
                print(f"ID: {user[0]}")
                print(f"  Ten dang nhap: {user[1]}")
                print(f"  Email: {user[2]}")
                print(f"  Ho ten: {user[3] or '(chua co)'}")
                print(f"  Ngay tao: {user[4]}")
                print(f"  Admin: {'Co' if user[5] else 'Khong'}")
                print()
        else:
            print("⚠️ Chua co nguoi dung nao")
            print()
            print("💡 De test:")
            print("   1. Chay ung dung: python chay_he_thong.py")
            print("   2. Mo trinh duyet: http://localhost:5000")
            print("   3. Dang ky tai khoan moi")
            print("   4. Chay lai script nay de kiem tra")
            print()
        
        # Kiểm tra bảng lich_su_giao_trinh
        print("=" * 60)
        print("BANG: lich_su_giao_trinh")
        print("=" * 60)
        
        cursor.execute("SELECT COUNT(*) FROM lich_su_giao_trinh")
        count = cursor.fetchone()[0]
        print(f"So luong ban ghi: {count}")
        print()
        
        if count > 0:
            cursor.execute("""
                SELECT ls.id, ls.chu_de, ls.ngay_tao, ls.do_dai_ky_tu, ls.da_xuat_file,
                       nd.ten_dang_nhap
                FROM lich_su_giao_trinh ls
                JOIN nguoi_dung nd ON ls.nguoi_dung_id = nd.id
                ORDER BY ls.ngay_tao DESC
                LIMIT 10
            """)
            histories = cursor.fetchall()
            
            print("10 ban ghi gan nhat:")
            print("-" * 60)
            for hist in histories:
                print(f"ID: {hist[0]}")
                print(f"  Chu de: {hist[1]}")
                print(f"  Nguoi dung: {hist[5]}")
                print(f"  Ngay tao: {hist[2]}")
                print(f"  Do dai: {hist[3]:,} ky tu")
                print(f"  Da xuat file: {'Co' if hist[4] else 'Chua'}")
                print()
        else:
            print("⚠️ Chua co lich su nao")
            print()
        
        conn.close()
        
        print("=" * 60)
        print("✅ Hoan tat kiem tra")
        print("=" * 60)
        
    except pymysql.Error as e:
        print(f"❌ Loi MySQL: {str(e)}")
        print()
        print("Kiem tra:")
        print("  1. MySQL da chay chua?")
        print("  2. Database 'giao_trinh_ai' da duoc tao chua?")
        print("  3. Cac bang da duoc tao chua?")
        print("  4. Thong tin trong .env co dung khong?")
    except Exception as e:
        print(f"❌ Loi: {str(e)}")


if __name__ == "__main__":
    try:
        kiem_tra_du_lieu()
    except KeyboardInterrupt:
        print("\n\n❌ Da huy boi nguoi dung")
    except Exception as e:
        print(f"\n❌ Loi: {str(e)}")
