from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from ung_dung.co_so_du_lieu.ket_noi import db


class NguoiDung(db.Model, UserMixin):
    """
    Model cho người dùng
    """
    __tablename__ = 'nguoi_dung'
    
    id = db.Column(db.Integer, primary_key=True)
    ten_dang_nhap = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    mat_khau_hash = db.Column(db.String(255), nullable=False)
    ho_ten = db.Column(db.String(100))
    ngay_tao = db.Column(db.DateTime, default=datetime.utcnow)
    la_admin = db.Column(db.Boolean, default=False)
    
    # Quan hệ với lịch sử
    lich_su = db.relationship('LichSuGiaoTrinh', backref='nguoi_dung', lazy=True, cascade='all, delete-orphan')
    
    def set_mat_khau(self, mat_khau):
        """Mã hóa mật khẩu"""
        self.mat_khau_hash = generate_password_hash(mat_khau)
    
    def kiem_tra_mat_khau(self, mat_khau):
        """Kiểm tra mật khẩu"""
        return check_password_hash(self.mat_khau_hash, mat_khau)
    
    def __repr__(self):
        return f'<NguoiDung {self.ten_dang_nhap}>'


class LichSuGiaoTrinh(db.Model):
    """
    Model cho lịch sử tạo giáo trình
    """
    __tablename__ = 'lich_su_giao_trinh'
    
    id = db.Column(db.Integer, primary_key=True)
    nguoi_dung_id = db.Column(db.Integer, db.ForeignKey('nguoi_dung.id'), nullable=False, index=True)
    chu_de = db.Column(db.String(200), nullable=False)
    noi_dung_html = db.Column(db.Text)
    duong_dan_file = db.Column(db.String(500))
    do_dai_ky_tu = db.Column(db.Integer, default=0)
    ngay_tao = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    da_xuat_file = db.Column(db.Boolean, default=False)
    
    def to_dict(self):
        """Chuyển đổi sang dictionary"""
        return {
            'id': self.id,
            'chu_de': self.chu_de,
            'do_dai_ky_tu': self.do_dai_ky_tu,
            'ngay_tao': self.ngay_tao.strftime('%d/%m/%Y %H:%M:%S'),
            'da_xuat_file': self.da_xuat_file,
            'duong_dan_file': self.duong_dan_file
        }
    
    def __repr__(self):
        return f'<LichSuGiaoTrinh {self.chu_de} - {self.ngay_tao}>'
