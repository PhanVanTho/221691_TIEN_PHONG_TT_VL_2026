from datetime import datetime
from ung_dung.co_so_du_lieu.mo_hinh import NguoiDung, LichSuGiaoTrinh
from ung_dung.co_so_du_lieu.ket_noi import db


def tao_nguoi_dung(ten_dang_nhap, email, mat_khau, ho_ten=None):
    """
    Tạo người dùng mới
    """
    # Kiểm tra trùng lặp
    if NguoiDung.query.filter_by(ten_dang_nhap=ten_dang_nhap).first():
        return None, "Tên đăng nhập đã tồn tại"
    
    if NguoiDung.query.filter_by(email=email).first():
        return None, "Email đã được sử dụng"
    
    # Tạo người dùng mới
    nguoi_dung = NguoiDung(
        ten_dang_nhap=ten_dang_nhap,
        email=email,
        ho_ten=ho_ten or ten_dang_nhap
    )
    nguoi_dung.set_mat_khau(mat_khau)
    
    try:
        db.session.add(nguoi_dung)
        db.session.commit()
        return nguoi_dung, None
    except Exception as e:
        db.session.rollback()
        return None, f"Lỗi khi tạo tài khoản: {str(e)}"


def xac_thuc_nguoi_dung(ten_dang_nhap, mat_khau):
    """
    Xác thực người dùng
    """
    nguoi_dung = NguoiDung.query.filter_by(ten_dang_nhap=ten_dang_nhap).first()
    
    if nguoi_dung and nguoi_dung.kiem_tra_mat_khau(mat_khau):
        return nguoi_dung
    return None


def luu_lich_su_giao_trinh(nguoi_dung_id, chu_de, noi_dung_html, duong_dan_file=None):
    """
    Lưu lịch sử tạo giáo trình
    """
    lich_su = LichSuGiaoTrinh(
        nguoi_dung_id=nguoi_dung_id,
        chu_de=chu_de,
        noi_dung_html=noi_dung_html,
        duong_dan_file=duong_dan_file,
        do_dai_ky_tu=len(noi_dung_html),
        da_xuat_file=bool(duong_dan_file)
    )
    
    try:
        db.session.add(lich_su)
        db.session.commit()
        return lich_su, None
    except Exception as e:
        db.session.rollback()
        return None, f"Lỗi khi lưu lịch sử: {str(e)}"


def lay_lich_su_nguoi_dung(nguoi_dung_id, gioi_han=50):
    """
    Lấy lịch sử tạo giáo trình của người dùng
    """
    return LichSuGiaoTrinh.query.filter_by(nguoi_dung_id=nguoi_dung_id)\
        .order_by(LichSuGiaoTrinh.ngay_tao.desc())\
        .limit(gioi_han)\
        .all()


def xoa_lich_su(lich_su_id, nguoi_dung_id):
    """
    Xóa một bản ghi lịch sử (chỉ của chính người dùng)
    """
    lich_su = LichSuGiaoTrinh.query.filter_by(id=lich_su_id, nguoi_dung_id=nguoi_dung_id).first()
    
    if lich_su:
        try:
            db.session.delete(lich_su)
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, f"Lỗi khi xóa: {str(e)}"
    
    return False, "Không tìm thấy bản ghi"
