from flask import Blueprint, request, render_template_string, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from ung_dung.co_so_du_lieu.thao_tac_du_lieu import tao_nguoi_dung, xac_thuc_nguoi_dung

xac_thuc = Blueprint('xac_thuc', __name__)


@xac_thuc.route('/dang-ky', methods=['GET', 'POST'])
def dang_ky():
    """Trang đăng ký"""
    if request.method == 'POST':
        ten_dang_nhap = request.form.get('ten_dang_nhap', '').strip()
        email = request.form.get('email', '').strip()
        mat_khau = request.form.get('mat_khau', '')
        ho_ten = request.form.get('ho_ten', '').strip()
        
        # Validation
        if not ten_dang_nhap or not email or not mat_khau:
            flash('Vui lòng điền đầy đủ thông tin', 'error')
            return render_template_string(dang_ky_template())
        
        if len(mat_khau) < 6:
            flash('Mật khẩu phải có ít nhất 6 ký tự', 'error')
            return render_template_string(dang_ky_template())
        
        # Tạo tài khoản
        nguoi_dung, loi = tao_nguoi_dung(ten_dang_nhap, email, mat_khau, ho_ten)
        
        if nguoi_dung:
            login_user(nguoi_dung)
            flash('Đăng ký thành công!', 'success')
            return redirect('/')
        else:
            flash(loi or 'Có lỗi xảy ra khi đăng ký', 'error')
            return render_template_string(dang_ky_template())
    
    return render_template_string(dang_ky_template())


@xac_thuc.route('/dang-nhap', methods=['GET', 'POST'])
def dang_nhap():
    """Trang đăng nhập"""
    if current_user.is_authenticated:
        return redirect(url_for('web.trang_chu'))
    
    if request.method == 'POST':
        ten_dang_nhap = request.form.get('ten_dang_nhap', '').strip()
        mat_khau = request.form.get('mat_khau', '')
        
        if not ten_dang_nhap or not mat_khau:
            flash('Vui lòng điền đầy đủ thông tin', 'error')
            return render_template_string(dang_nhap_template())
        
        nguoi_dung = xac_thuc_nguoi_dung(ten_dang_nhap, mat_khau)
        
        if nguoi_dung:
            login_user(nguoi_dung, remember=True)
            flash(f'Chào mừng {nguoi_dung.ho_ten}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/')
        else:
            flash('Tên đăng nhập hoặc mật khẩu không đúng', 'error')
            return render_template_string(dang_nhap_template())
    
    return render_template_string(dang_nhap_template())


@xac_thuc.route('/dang-xuat')
@login_required
def dang_xuat():
    """Đăng xuất"""
    logout_user()
    flash('Đã đăng xuất thành công', 'info')
    return redirect(url_for('xac_thuc.dang_nhap'))


def dang_nhap_template():
    """Template HTML cho trang đăng nhập"""
    return """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Đăng nhập - Hệ thống giáo trình AI</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .auth-container {
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            padding: 40px;
            width: 100%;
            max-width: 400px;
        }
        h1 {
            text-align: center;
            color: #667eea;
            margin-bottom: 30px;
            font-size: 2em;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            color: #555;
            font-weight: 500;
        }
        input[type="text"],
        input[type="email"],
        input[type="password"] {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 6px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        input:focus {
            outline: none;
            border-color: #667eea;
        }
        .btn {
            width: 100%;
            padding: 12px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
        }
        .btn:hover {
            transform: translateY(-2px);
        }
        .links {
            text-align: center;
            margin-top: 20px;
        }
        .links a {
            color: #667eea;
            text-decoration: none;
        }
        .links a:hover {
            text-decoration: underline;
        }
        .alert {
            padding: 12px;
            border-radius: 6px;
            margin-bottom: 20px;
        }
        .alert-error { background: #ffebee; color: #c62828; border: 1px solid #f44336; }
        .alert-success { background: #e8f5e9; color: #2e7d32; border: 1px solid #4caf50; }
        .alert-info { background: #e3f2fd; color: #1565c0; border: 1px solid #2196f3; }
    </style>
</head>
<body>
    <div class="auth-container">
        <h1>🔐 Đăng nhập</h1>
        
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        <form method="POST">
            <div class="form-group">
                <label>Tên đăng nhập</label>
                <input type="text" name="ten_dang_nhap" required autofocus>
            </div>
            <div class="form-group">
                <label>Mật khẩu</label>
                <input type="password" name="mat_khau" required>
            </div>
            <button type="submit" class="btn">Đăng nhập</button>
        </form>
        
        <div class="links">
            <p>Chưa có tài khoản? <a href="/dang-ky">Đăng ký ngay</a></p>
            <p><a href="/">← Về trang chủ</a></p>
        </div>
    </div>
</body>
</html>
"""


def dang_ky_template():
    """Template HTML cho trang đăng ký"""
    return """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Đăng ký - Hệ thống giáo trình AI</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .auth-container {
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            padding: 40px;
            width: 100%;
            max-width: 400px;
        }
        h1 {
            text-align: center;
            color: #667eea;
            margin-bottom: 30px;
            font-size: 2em;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            color: #555;
            font-weight: 500;
        }
        input[type="text"],
        input[type="email"],
        input[type="password"] {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 6px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        input:focus {
            outline: none;
            border-color: #667eea;
        }
        .btn {
            width: 100%;
            padding: 12px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 6px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
        }
        .btn:hover {
            transform: translateY(-2px);
        }
        .links {
            text-align: center;
            margin-top: 20px;
        }
        .links a {
            color: #667eea;
            text-decoration: none;
        }
        .links a:hover {
            text-decoration: underline;
        }
        .alert {
            padding: 12px;
            border-radius: 6px;
            margin-bottom: 20px;
        }
        .alert-error { background: #ffebee; color: #c62828; border: 1px solid #f44336; }
        .alert-success { background: #e8f5e9; color: #2e7d32; border: 1px solid #4caf50; }
    </style>
</head>
<body>
    <div class="auth-container">
        <h1>📝 Đăng ký</h1>
        
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        <form method="POST">
            <div class="form-group">
                <label>Họ và tên</label>
                <input type="text" name="ho_ten" placeholder="Nguyễn Văn A">
            </div>
            <div class="form-group">
                <label>Tên đăng nhập *</label>
                <input type="text" name="ten_dang_nhap" required autofocus>
            </div>
            <div class="form-group">
                <label>Email *</label>
                <input type="email" name="email" required>
            </div>
            <div class="form-group">
                <label>Mật khẩu *</label>
                <input type="password" name="mat_khau" required minlength="6">
            </div>
            <button type="submit" class="btn">Đăng ký</button>
        </form>
        
        <div class="links">
            <p>Đã có tài khoản? <a href="/dang-nhap">Đăng nhập</a></p>
            <p><a href="/">← Về trang chủ</a></p>
        </div>
    </div>
</body>
</html>
"""
