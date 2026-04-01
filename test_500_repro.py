import sys
import os
from dotenv import load_dotenv

# Load env before imports
load_dotenv()

# Add project root to path
sys.path.append(os.getcwd())

from ung_dung.xu_ly_ai.tao_giao_trinh import tao_giao_trinh
from ung_dung.dich_vu.xuat_docx import xuat_giao_trinh_docx # Note: chay_he_thong has its own xuat_docx logic, we should test tao_giao_trinh primarily

def test_repro():
    chu_de = "Trân Tạo:1" # The topic from the error URL
    print(f"Testing with topic: {chu_de}")

    try:
        print("1. Calling tao_giao_trinh...")
        kq = tao_giao_trinh(chu_de)
        print("   -> tao_giao_trinh returned keys:", kq.keys())
        
        if "noi_dung" in kq:
            print(f"   -> Content length: {len(kq['noi_dung'])}")
            if "error-message" in kq["noi_dung"]:
                 print("   -> Returned ERROR HTML")
            else:
                 print("   -> Returned Content HTML")
        
    except Exception as e:
        print("!!! CRASH in tao_giao_trinh !!!")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_repro()
