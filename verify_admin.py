from flask import Flask
from ung_dung.co_so_du_lieu.ket_noi import khoi_tao_db, db
from ung_dung.co_so_du_lieu.mo_hinh import NguoiDung
from ung_dung.admin_setup import init_admin_account
import os

# Mock App
app = Flask(__name__)
# Ensure we use the same DB URI as real app or a test one. 
# Assuming config is loaded via dotenv in khoi_tao_db or globally.
# Let's load .env manually to be safe if khoi_tao_db relies on it being loaded before.
from dotenv import load_dotenv
load_dotenv()

khoi_tao_db(app)

with app.app_context():
    print("Running init_admin_account()...")
    init_admin_account()
    
    print("Verifying admin user...")
    admin = NguoiDung.query.filter_by(ten_dang_nhap='admin').first()
    if admin:
        print(f"✅ Admin found: {admin.ten_dang_nhap}")
        print(f"✅ Is Admin? {admin.la_admin}")
        print(f"✅ Password Check (12345678): {admin.kiem_tra_mat_khau('12345678')}")
    else:
        print("❌ Admin user NOT found!")
