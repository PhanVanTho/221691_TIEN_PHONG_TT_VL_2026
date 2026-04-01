from flask import Blueprint, request, jsonify
from datetime import datetime
import uuid

from ung_dung.thu_thap_du_lieu.quet_wiki import lay_noi_dung_wikipedia
from ung_dung.thu_thap_du_lieu.lam_sach_van_ban import lam_sach_van_ban
from ung_dung.xu_ly_ai.tao_giao_trinh import tao_giao_trinh
from ung_dung.dich_vu.xuat_docx import xuat_giao_trinh_docx


api = Blueprint("api", __name__)

# =========================
# GIẢ LẬP KHO GIÁO TRÌNH
# =========================
GIAO_TRINH_DB = {}


# =========================
# KIỂM TRA API
# =========================
@api.route("/", methods=["GET"])
def kiem_tra_api():
    return "API GIAO TRINH AI DANG HOAT DONG OK"


# =========================
# TẠO GIÁO TRÌNH (KHÔNG LƯU)
# =========================
@api.route("/tao-giao-trinh", methods=["GET"])
def tao_giao_trinh_ai():
    chu_de = request.args.get("chu_de", "").strip()

    if not chu_de:
        return jsonify({"loi": "Vui long truyen ?chu_de=TenChuDe"}), 400

    try:
        ket_qua = tao_giao_trinh(chu_de)
        return jsonify(ket_qua)
    except Exception as e:
        return jsonify({"loi": f"Lỗi khi tạo giáo trình: {str(e)}"}), 500


# =========================
# TẠO GIÁO TRÌNH + LƯU KHO
# =========================
@api.route("/tao-giao-trinh-va-luu", methods=["GET"])
def tao_va_luu():
    chu_de = request.args.get("chu_de", "").strip()

    if not chu_de:
        return jsonify({"loi": "Vui long truyen ?chu_de=TenChuDe"}), 400

    try:
        ket_qua = tao_giao_trinh(chu_de)
        noi_dung = ket_qua.get("noi_dung", "")

    ma_gt = str(uuid.uuid4())

        giao_trinh = {
            "id": ma_gt,
            "chu_de": chu_de,
            "noi_dung": noi_dung,
            "do_dai_ky_tu": len(noi_dung),
            "thoi_gian_tao": datetime.now().isoformat()
        }

        GIAO_TRINH_DB[ma_gt] = giao_trinh
        return jsonify(giao_trinh)
    except Exception as e:
        return jsonify({"loi": f"Lỗi khi tạo và lưu giáo trình: {str(e)}"}), 500


# =========================
# LẤY GIÁO TRÌNH ĐÃ LƯU
# =========================
@api.route("/lay-giao-trinh/<ma_gt>", methods=["GET"])
def lay_giao_trinh(ma_gt):
    giao_trinh = GIAO_TRINH_DB.get(ma_gt)

    if not giao_trinh:
        return jsonify({"loi": "Khong tim thay giao trinh"}), 404

    return jsonify(giao_trinh)


# =========================
# THU THẬP + LÀM SẠCH WIKIPEDIA
# =========================
@api.route("/thu-thap-wiki", methods=["GET"])
def thu_thap_wiki():
    chu_de = request.args.get("chu_de", "").strip()

    if not chu_de:
        return jsonify({"loi": "Vui long truyen ?chu_de=TenChuDe"}), 400

    try:
        noi_dung_tho = lay_noi_dung_wikipedia(chu_de)
        noi_dung_sach = lam_sach_van_ban(noi_dung_tho)

        return jsonify({
            "chu_de": chu_de,
            "do_dai_ky_tu": len(noi_dung_sach),
            "noi_dung_xem_truoc": noi_dung_sach[:2000]
        })
    except Exception as e:
        return jsonify({"loi": f"Lỗi khi thu thập dữ liệu: {str(e)}"}), 500


# =========================
# XUẤT GIÁO TRÌNH DOCX
# =========================
@api.route("/xuat-giao-trinh-docx", methods=["GET"])
def xuat_giao_trinh():
    chu_de = request.args.get("chu_de", "").strip()

    if not chu_de:
        return jsonify({"loi": "Vui long truyen ?chu_de=TenChuDe"}), 400

    try:
        ket_qua = tao_giao_trinh(chu_de)
        noi_dung = ket_qua.get("noi_dung", "")

        duong_dan = xuat_giao_trinh_docx(chu_de, noi_dung)

        return jsonify({
            "chu_de": chu_de,
            "file": duong_dan,
            "trang_thai": "Xuat giao trinh thanh cong"
        })
    except Exception as e:
        return jsonify({"loi": f"Lỗi khi xuất file: {str(e)}"}), 500
