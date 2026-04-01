from flask import Blueprint, request
from ung_dung.xu_ly_ai.tao_giao_trinh import tao_giao_trinh

web = Blueprint("web", __name__)


@web.route("/", methods=["GET", "POST"])
def trang_chu():
    noi_dung_html = ""

    if request.method == "POST":
        chu_de = request.form.get("chu_de", "").strip()

        if chu_de:
            ket_qua = tao_giao_trinh(chu_de)
            noi_dung = ket_qua["noi_dung"]

            # Hiển thị xuống dòng đẹp
            noi_dung_html = "<br>".join(noi_dung.split("\n"))

    return f"""
    <html>
    <head>
        <meta charset="utf-8">
        <title>Hệ thống giáo trình AI</title>
    </head>
    <body>
        <h1>HỆ THỐNG XÂY DỰNG GIÁO TRÌNH TỰ ĐỘNG SỬ DỤNG AI</h1>

        <form method="post">
            <label><b>Nhập chủ đề giáo trình:</b></label><br><br>
            <input type="text" name="chu_de" style="width:400px" required>
            <br><br>
            <button type="submit">🚀 Tạo giáo trình</button>
        </form>

        <hr>

        <div>
            {noi_dung_html}
        </div>
    </body>
    </html>
    """
