def dinh_dang_bai_hoc(noi_dung):
    return {
        "muc_tieu": noi_dung.get("muc_tieu"),
        "khai_niem": noi_dung.get("khai_niem"),
        "noi_dung": noi_dung.get("noi_dung"),
        "vi_du": noi_dung.get("vi_du"),
        "cau_hoi": noi_dung.get("cau_hoi"),
        "tai_lieu": noi_dung.get("tai_lieu")
    }
