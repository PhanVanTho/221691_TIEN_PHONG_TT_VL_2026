from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import os

# Load biến môi trường từ file .env
load_dotenv()

db = SQLAlchemy()
login_manager = LoginManager()

def khoi_tao_db(app):
    """
    Khởi tạo database và cấu hình
    Hỗ trợ cả SQLite (lưu trong máy) và MySQL (lưu trên server)
    """
    # Kiểm tra loại database từ biến môi trường
    db_type = os.getenv('DB_TYPE', 'sqlite').lower()
    
    if db_type == 'mysql':
        # Cấu hình MySQL
        db_host = os.getenv('DB_HOST', 'localhost')
        db_port = os.getenv('DB_PORT', '3306')
        db_user = os.getenv('DB_USER', 'root')
        db_password = os.getenv('DB_PASSWORD', '')
        db_name = os.getenv('DB_NAME', 'giao_trinh_ai')
        
        app.config['SQLALCHEMY_DATABASE_URI'] = (
            f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
        )
        print(f"✅ Đang kết nối MySQL: {db_host}:{db_port}/{db_name}")
    else:
        # Cấu hình SQLite (mặc định - lưu trong máy)
        basedir = os.path.abspath(os.path.dirname(__file__))
        db_path = os.path.join(basedir, '..', '..', '..', 'database.db')
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
        print(f"✅ Đang sử dụng SQLite (lưu trong máy): {db_path}")
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Khởi tạo extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'xac_thuc.dang_nhap'
    login_manager.login_message = 'Vui lòng đăng nhập để tiếp tục.'
    login_manager.login_message_category = 'info'
    
    # Tạo tables
    with app.app_context():
        try:
            db.create_all()
            print("✅ Đã tạo/kiểm tra database tables thành công")
        except Exception as e:
            print(f"⚠️ Lỗi khi tạo tables: {str(e)}")
            if db_type == 'mysql':
                print("💡 Hãy đảm bảo MySQL đã được cài đặt và database đã được tạo")
                print("💡 Chạy lệnh: CREATE DATABASE giao_trinh_ai;")
    
    return db, login_manager
