from ung_dung.co_so_du_lieu.mo_hinh import NguoiDung
from ung_dung.co_so_du_lieu.ket_noi import db

def init_admin_account():
    """
    Khởi tạo tài khoản admin mặc định nếu chưa tồn tại
    """
    try:
        admin_user = NguoiDung.query.filter_by(ten_dang_nhap='admin').first()
        if not admin_user:
            print("Creating default admin account...")
            admin_user = NguoiDung(
                ten_dang_nhap='admin',
                email='admin@system.local',
                ho_ten='System Administrator',
                la_admin=True
            )
            admin_user.set_mat_khau('12345678')
            db.session.add(admin_user)
            db.session.commit()
            print("Admin account created: admin / 12345678")
        else:
            # Ensure existing admin retains admin privileges
            if not admin_user.la_admin:
                admin_user.la_admin = True
                db.session.commit()
                print("Updated existing 'admin' user to have admin privileges.")
    except Exception as e:
        print(f"Error initializing admin account: {e}")
