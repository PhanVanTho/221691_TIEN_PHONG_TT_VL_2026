from flask import Blueprint, render_template, render_template_string, redirect, url_for, flash, request
from flask_login import login_required, current_user
from functools import wraps
from ung_dung.co_so_du_lieu.mo_hinh import NguoiDung, LichSuGiaoTrinh
from ung_dung.co_so_du_lieu.ket_noi import db
from ung_dung.co_so_du_lieu.thao_tac_du_lieu import tao_nguoi_dung

quan_tri = Blueprint('quan_tri', __name__, template_folder='templates')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.la_admin:
            flash("Bạn không có quyền truy cập trang này.", "error")
            return redirect(url_for('xac_thuc.dang_nhap'))
        return f(*args, **kwargs)
    return decorated_function

# --- ROUTES ---

@quan_tri.route('/')
@login_required
@admin_required
def dashboard():
    """Trang chủ Admin Dashboard"""
    so_luong_users = NguoiDung.query.count()
    so_luong_giao_trinh = LichSuGiaoTrinh.query.count()
    giao_trinh_moi_nhat = LichSuGiaoTrinh.query.order_by(LichSuGiaoTrinh.ngay_tao.desc()).limit(5).all()
    
    return render_template_string(dashboard_template(), 
                                  so_luong_users=so_luong_users, 
                                  so_luong_giao_trinh=so_luong_giao_trinh,
                                  giao_trinh_moi_nhat=giao_trinh_moi_nhat)

@quan_tri.route('/nguoi-dung')
@login_required
@admin_required
def quan_ly_nguoi_dung():
    """Danh sách người dùng"""
    users = NguoiDung.query.all()
    return render_template_string(user_list_template(), users=users)

@quan_tri.route('/nguoi-dung/them', methods=['POST'])
@login_required
@admin_required
def them_nguoi_dung():
    """Thêm người dùng mới (hoặc admin)"""
    ten_dang_nhap = request.form.get('ten_dang_nhap')
    email = request.form.get('email')
    mat_khau = request.form.get('mat_khau')
    ho_ten = request.form.get('ho_ten')
    la_admin = request.form.get('la_admin') == 'on'

    if not ten_dang_nhap or not email or not mat_khau:
        flash("Vui lòng điền đầy đủ thông tin", "error")
        return redirect(url_for('quan_tri.quan_ly_nguoi_dung'))

    user, error = tao_nguoi_dung(ten_dang_nhap, email, mat_khau, ho_ten)
    if error:
        flash(error, "error")
    else:
        if la_admin:
            user.la_admin = True
            db.session.commit()
        flash("Thêm người dùng thành công", "success")
    
    return redirect(url_for('quan_tri.quan_ly_nguoi_dung'))

@quan_tri.route('/giao-trinh')
@login_required
@admin_required
def quan_ly_giao_trinh():
    """Danh sách toàn bộ giáo trình"""
    page = request.args.get('page', 1, type=int)
    giao_trinhs = LichSuGiaoTrinh.query.order_by(LichSuGiaoTrinh.ngay_tao.desc()).paginate(page=page, per_page=20)
    return render_template_string(curriculum_list_template(), giao_trinhs=giao_trinhs)

# --- TEMPLATES (Embedded for simplicity, generally should be in separate files) ---

def base_admin_template(content, title="Admin Dashboard"):
    return f"""
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="utf-8">
    <title>{title} - Quản trị hệ thống</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        :root {{ --primary: #4f46e5; --secondary: #64748b; --bg: #f1f5f9; }}
        body {{ font-family: 'Segoe UI', sans-serif; margin: 0; background: var(--bg); display: flex; min-height: 100vh; }}
        .sidebar {{ width: 250px; background: white; border-right: 1px solid #e2e8f0; position: fixed; height: 100%; top: 0; left: 0; }}
        .sidebar-header {{ padding: 20px; border-bottom: 1px solid #e2e8f0; font-weight: bold; color: var(--primary); font-size: 1.2em; }}
        .nav-link {{ display: block; padding: 15px 20px; color: var(--secondary); text-decoration: none; transition: 0.2s; }}
        .nav-link:hover, .nav-link.active {{ background: #eff6ff; color: var(--primary); border-right: 3px solid var(--primary); }}
        .nav-link i {{ width: 25px; }}
        .main-content {{ margin-left: 250px; flex: 1; padding: 30px; }}
        .card {{ background: white; border-radius: 10px; padding: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); margin-bottom: 20px; }}
        .header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }}
        .btn {{ padding: 8px 16px; border-radius: 6px; border: none; cursor: pointer; font-weight: 500; text-decoration: none; display: inline-block; }}
        .btn-primary {{ background: var(--primary); color: white; }}
        .btn-danger {{ background: #ef4444; color: white; }}
        .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }}
        .stat-card {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
        .stat-value {{ font-size: 2em; font-weight: bold; color: var(--primary); margin: 10px 0; }}
        .stat-label {{ color: var(--secondary); }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #e2e8f0; }}
        th {{ color: var(--secondary); font-weight: 600; font-size: 0.9em; }}
        .badge {{ padding: 4px 8px; border-radius: 4px; font-size: 0.8em; font-weight: bold; }}
        .badge-admin {{ background: #dbeafe; color: #1e40af; }}
        .badge-user {{ background: #f1f5f9; color: #475569; }}
        .alert {{ padding: 15px; border-radius: 6px; margin-bottom: 20px; }}
        .alert-error {{ background: #fee2e2; color: #991b1b; }}
        .alert-success {{ background: #dcfce7; color: #166534; }}
    </style>
</head>
<body>
    <div class="sidebar">
        <div class="sidebar-header"><i class="fas fa-shield-alt"></i> Admin Panel</div>
        <nav>
            <a href="/admin/" class="nav-link"><i class="fas fa-home"></i> Tổng quan</a>
            <a href="/admin/nguoi-dung" class="nav-link"><i class="fas fa-users"></i> Người dùng</a>
            <a href="/admin/giao-trinh" class="nav-link"><i class="fas fa-book"></i> Giáo trình</a>
            <a href="/" class="nav-link"><i class="fas fa-external-link-alt"></i> Xem trang chủ</a>
            <a href="/dang-xuat" class="nav-link" style="color: #ef4444;"><i class="fas fa-sign-out-alt"></i> Đăng xuất</a>
        </nav>
    </div>
    <div class="main-content">
        <!-- Flash Messages -->
        {{% with messages = get_flashed_messages(with_categories=true) %}}
            {{% if messages %}}
                {{% for category, message in messages %}}
                    <div class="alert alert-{{{{ category }}}}">{{{{ message }}}}</div>
                {{% endfor %}}
            {{% endif %}}
        {{% endwith %}}
        
        {content}
    </div>
</body>
</html>
"""

def dashboard_template():
    content = """
    <div class="header">
        <h2>Tổng quan hệ thống</h2>
        <span style="color: #64748b;">Xin chào, {{ current_user.ho_ten }}</span>
    </div>

    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-label">Tổng người dùng</div>
            <div class="stat-value">{{ so_luong_users }}</div>
            <div style="font-size: 0.8em; color: #10b981;"><i class="fas fa-arrow-up"></i> Đang hoạt động</div>
        </div>
        <div class="stat-card">
            <div class="stat-label">Giáo trình đã tạo</div>
            <div class="stat-value">{{ so_luong_giao_trinh }}</div>
            <div style="font-size: 0.8em; color: #3b82f6;"><i class="fas fa-book-open"></i> Tài liệu</div>
        </div>
    </div>

    <div class="card">
        <h3><i class="fas fa-clock"></i> Hoạt động gần đây</h3>
        <table>
            <thead>
                <tr>
                    <th>Người dùng</th>
                    <th>Chủ đề</th>
                    <th>Thời gian</th>
                    <th>Trạng thái</th>
                </tr>
            </thead>
            <tbody>
                {% for gt in giao_trinh_moi_nhat %}
                <tr>
                    <td>{{ gt.nguoi_dung.ho_ten }}</td>
                    <td>{{ gt.chu_de }}</td>
                    <td>{{ gt.ngay_tao.strftime('%d/%m/%Y %H:%M') }}</td>
                    <td>
                        {% if gt.da_xuat_file %}
                            <span style="color: #10b981;"><i class="fas fa-check"></i> Đã xuất</span>
                        {% else %}
                            <span style="color: #f59e0b;">Lưu tạm</span>
                        {% endif %}
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
    """
    return base_admin_template(content)

def user_list_template():
    content = """
    <div class="header">
        <h2>Quản lý người dùng</h2>
    </div>

    <div class="card" style="background: #f8fafc; border: 1px dashed #cbd5e1;">
        <h4 style="margin-top: 0;">Thêm thành viên mới</h4>
        <form action="{{ url_for('quan_tri.them_nguoi_dung') }}" method="POST" style="display: flex; gap: 10px; align-items: center; flex-wrap: wrap;">
            <input type="text" name="ho_ten" placeholder="Họ tên" required style="padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
            <input type="text" name="ten_dang_nhap" placeholder="Username" required style="padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
            <input type="email" name="email" placeholder="Email" required style="padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
            <input type="password" name="mat_khau" placeholder="Mật khẩu" required style="padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
            <label style="display: flex; align-items: center; gap: 5px; font-size: 0.9em;">
                <input type="checkbox" name="la_admin"> Admin?
            </label>
            <button type="submit" class="btn btn-primary"><i class="fas fa-plus"></i> Thêm</button>
        </form>
    </div>

    <div class="card">
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Họ tên</th>
                    <th>Username</th>
                    <th>Email</th>
                    <th>Vai trò</th>
                    <th>Ngày tham gia</th>
                </tr>
            </thead>
            <tbody>
                {% for user in users %}
                <tr>
                    <td>#{{ user.id }}</td>
                    <td>
                        <div style="font-weight: 500;">{{ user.ho_ten }}</div>
                    </td>
                    <td>{{ user.ten_dang_nhap }}</td>
                    <td>{{ user.email }}</td>
                    <td>
                        {% if user.la_admin %}
                            <span class="badge badge-admin">Admin</span>
                        {% else %}
                            <span class="badge badge-user">Member</span>
                        {% endif %}
                    </td>
                    <td>{{ user.ngay_tao.strftime('%d/%m/%Y') }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
    """
    return base_admin_template(content, "Người dùng")

def curriculum_list_template():
    content = """
    <div class="header">
        <h2>Lịch sử giáo trình toàn hệ thống</h2>
    </div>

    <div class="card">
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Người tạo</th>
                    <th>Chủ đề</th>
                    <th>Ngày tạo</th>
                    <th>File</th>
                </tr>
            </thead>
            <tbody>
                {% for gt in giao_trinhs.items %}
                <tr>
                    <td>#{{ gt.id }}</td>
                    <td>
                        <div style="font-weight: 500;">{{ gt.nguoi_dung.ho_ten }}</div>
                        <div style="font-size: 0.8em; color: #64748b;">{{ gt.nguoi_dung.email }}</div>
                    </td>
                    <td>
                        <div style="font-weight: 500;">{{ gt.chu_de }}</div>
                        <div style="font-size: 0.8em; color: #64748b;">{{ "{:,}".format(gt.do_dai_ky_tu) }} ký tự</div>
                    </td>
                    <td>{{ gt.ngay_tao.strftime('%d/%m/%Y %H:%M') }}</td>
                    <td>
                        {% if gt.da_xuat_file %}
                            <a href="#" class="btn btn-primary" style="font-size: 0.8em; padding: 4px 8px;"><i class="fas fa-download"></i> Tải về</a>
                        {% else %}
                            <span style="color: #94a3b8;">Chưa xuất</span>
                        {% endif %}
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>

        <!-- Pagination -->
        <div style="margin-top: 20px; display: flex; gap: 5px; justify-content: center;">
            {% if giao_trinhs.has_prev %}
                <a href="{{ url_for('quan_tri.quan_ly_giao_trinh', page=giao_trinhs.prev_num) }}" class="btn" style="background: #e2e8f0;">&laquo; Trước</a>
            {% endif %}
            <span style="padding: 8px 12px;">Trang {{ giao_trinhs.page }} / {{ giao_trinhs.pages }}</span>
            {% if giao_trinhs.has_next %}
                <a href="{{ url_for('quan_tri.quan_ly_giao_trinh', page=giao_trinhs.next_num) }}" class="btn" style="background: #e2e8f0;">Sau &raquo;</a>
            {% endif %}
        </div>
    </div>
    """
    return base_admin_template(content, "Giáo trình")
