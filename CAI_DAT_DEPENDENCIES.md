# 📦 Hướng dẫn cài đặt Dependencies

## ⚠️ Lỗi: ModuleNotFoundError

Nếu gặp lỗi `ModuleNotFoundError: No module named 'xxx'`, bạn cần cài đặt dependencies.

---

## 🚀 Cách 1: Cài đặt tất cả (Khuyến nghị)

```bash
cd he_thong_giao_trinh_ai
pip install -r requirements.txt
```

Hoặc:

```bash
python -m pip install -r requirements.txt
```

---

## 🚀 Cách 2: Sử dụng Virtual Environment (Tốt nhất)

### Tạo virtual environment:

```bash
cd he_thong_giao_trinh_ai
python -m venv env
```

### Kích hoạt virtual environment:

**Windows:**
```bash
env\Scripts\activate
```

**Linux/Mac:**
```bash
source env/bin/activate
```

### Cài đặt dependencies:

```bash
pip install -r requirements.txt
```

### Chạy ứng dụng:

```bash
python chay_he_thong.py
```

---

## 📋 Danh sách Dependencies

Các package cần thiết (trong `requirements.txt`):

- `flask>=2.3.0` - Web framework
- `flask-sqlalchemy>=3.0.0` - ORM cho database
- `flask-login>=0.6.3` - Quản lý đăng nhập
- `werkzeug>=2.3.0` - WSGI utilities
- `requests>=2.31.0` - HTTP library
- `python-dotenv>=1.0.0` - Load biến môi trường từ .env
- `google-generativeai>=0.3.0` - Google Gemini AI
- `python-docx>=1.1.0` - Xử lý file Word
- `pymysql>=1.1.0` - MySQL driver
- `cryptography>=41.0.0` - Mã hóa (cần cho pymysql)

---

## ✅ Kiểm tra đã cài đặt

Chạy lệnh để kiểm tra:

```bash
python -c "import flask; import flask_sqlalchemy; import flask_login; import dotenv; print('✅ Tất cả dependencies đã được cài đặt')"
```

---

## 🔧 Xử lý lỗi

### Lỗi: "pip is not recognized"

**Giải pháp:**
```bash
python -m pip install -r requirements.txt
```

### Lỗi: "Permission denied"

**Giải pháp:**
- Windows: Chạy Command Prompt as Administrator
- Linux/Mac: Dùng `sudo` (không khuyến nghị) hoặc dùng virtual environment

### Lỗi: "No module named 'dotenv'"

**Giải pháp:**
```bash
pip install python-dotenv
```

---

## 💡 Tips

1. **Luôn dùng virtual environment** cho mỗi dự án
2. **Cập nhật requirements.txt** khi thêm package mới:
   ```bash
   pip freeze > requirements.txt
   ```
3. **Kiểm tra Python version**: Cần Python 3.7+

---

## 🎯 Sau khi cài đặt

1. Kiểm tra file `.env` đã cấu hình MySQL chưa
2. Chạy ứng dụng: `python chay_he_thong.py`
3. Kiểm tra console có hiển thị kết nối MySQL không
