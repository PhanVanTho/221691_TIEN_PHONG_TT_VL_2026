from ung_dung.thu_thap_du_lieu.quet_wiki import lay_noi_dung_wikipedia
from ung_dung.thu_thap_du_lieu.lam_sach_van_ban import lam_sach_van_ban
from ung_dung.cot_loi.mau_lenh_ai import prompt_bai_hoc
from ung_dung.cot_loi.ket_noi_ai import goi_ai

def tao_giao_trinh(chu_de):
    raw = lay_noi_dung_wikipedia(chu_de)
    sach = lam_sach_van_ban(raw)
    prompt = prompt_bai_hoc(chu_de, sach)
    ket_qua = goi_ai(prompt)
    return {"chu_de": chu_de, "noi_dung": ket_qua}
