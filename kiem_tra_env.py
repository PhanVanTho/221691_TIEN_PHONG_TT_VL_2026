"""
Script kiểm tra file .env và cấu hình
"""
import os
from dotenv import load_dotenv

def kiem_tra_env():
    """Kiểm tra cấu hình .env"""
    
    print("=" * 60)
    print("KIEM TRA FILE .ENV")
    print("=" * 60)
    print()
    
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    
    if not os.path.exists(env_path):
        print("❌ Khong tim thay file .env")
        print()
        print("💡 Tao file .env voi noi dung:")
        print("   DB_TYPE=mysql")
        print("   DB_HOST=localhost")
        print("   DB_PORT=3306")
        print("   DB_USER=root")
        print("   DB_PASSWORD=")
        print("   DB_NAME=giao_trinh_ai")
        return
    
    print(f"✅ Tim thay file .env: {env_path}")
    print()
    
    # Load .env
    load_dotenv(env_path)
    
    # Kiểm tra các biến
    print("Cac bien moi truong:")
    print("-" * 60)
    
    db_type = os.getenv('DB_TYPE', 'NOT SET')
    db_host = os.getenv('DB_HOST', 'NOT SET')
    db_port = os.getenv('DB_PORT', 'NOT SET')
    db_user = os.getenv('DB_USER', 'NOT SET')
    db_password = os.getenv('DB_PASSWORD', 'NOT SET')
    db_name = os.getenv('DB_NAME', 'NOT SET')
    
    print(f"DB_TYPE      = {db_type}")
    print(f"DB_HOST      = {db_host}")
    print(f"DB_PORT      = {db_port}")
    print(f"DB_USER      = {db_user}")
    print(f"DB_PASSWORD  = {'***' if db_password else '(empty)'}")
    print(f"DB_NAME      = {db_name}")
    print()
    
    # Đánh giá
    print("=" * 60)
    print("DANH GIA:")
    print("=" * 60)
    
    if db_type.lower() == 'mysql':
        print("✅ DB_TYPE = mysql (Dung MySQL)")
        if db_host != 'NOT SET' and db_name != 'NOT SET':
            print("✅ Cac thong tin MySQL da duoc cau hinh")
            print()
            print("💡 Khi chay ung dung, ban se thay:")
            print(f"   ✅ Dang ket noi MySQL: {db_host}:{db_port}/{db_name}")
        else:
            print("⚠️ Thieu thong tin MySQL")
    else:
        print("⚠️ DB_TYPE khong phai 'mysql'")
        print(f"   Hien tai: {db_type}")
        print()
        print("💡 De dung MySQL, them vao file .env:")
        print("   DB_TYPE=mysql")
    
    print()
    print("=" * 60)


if __name__ == "__main__":
    try:
        kiem_tra_env()
    except Exception as e:
        print(f"❌ Loi: {str(e)}")
