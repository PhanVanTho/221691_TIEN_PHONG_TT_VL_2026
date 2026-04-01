import requests
import re

WIKI_API_URL_VI = "https://vi.wikipedia.org/w/api.php"
WIKI_API_URL_EN = "https://en.wikipedia.org/w/api.php"

HEADERS = {
    "User-Agent": "HeThongGiaoTrinhAI/2.0 (Upgrade; Contact: admin@example.com)"
}

def call_wiki_api(url, params):
    try:
        response = requests.get(url, params=params, headers=HEADERS, timeout=20)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error calling Wiki API: {e}")
    return {}

def lay_noi_dung_va_anh(url_api, title, chars=None):
    """Lấy nội dung và danh sách ảnh thumbnail của bài viết"""
    try:
        params = {
            "action": "query",
            "format": "json",
            "prop": "extracts|pageimages",
            "explaintext": True,
            "titles": title,
            "redirects": 1,
            "pithumbsize": 600
        }
        if chars:
            params["exchars"] = chars

        data = call_wiki_api(url_api, params)
        if not data: return "", []
        
        pages = data.get("query", {}).get("pages", {})
        
        content = ""
        images = []
        
        for _, page in pages.items():
            content = page.get("extract", "")
            # Defensive check for NoneType error
            thumb = page.get("thumbnail")
            if thumb and isinstance(thumb, dict):
                src = thumb.get("source")
                if src: images.append(src)
                
        return content, images
    except Exception as e:
        print(f"Error in lay_noi_dung_va_anh ({title}): {e}")
        return "", []

def tim_kiem_tieu_de(url_api, query):
    """Tìm tiêu đề bài viết từ từ khóa"""
    try:
        params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json"
        }
        data = call_wiki_api(url_api, params)
        search_results = data.get("query", {}).get("search", [])
        
        if search_results and isinstance(search_results, list) and len(search_results) > 0:
            item = search_results[0]
            if item and isinstance(item, dict):
                return item.get("title")
        return None
    except Exception as e:
        print(f"Error in tim_kiem_tieu_de ({query}): {e}")
        return None

def lay_lien_ket_ngon_ngu(title_vi):
    """Lấy tiêu đề bài viết tương ứng trên Wiki tiếng Anh"""
    try:
        params = {
            "action": "query",
            "format": "json",
            "prop": "langlinks",
            "titles": title_vi,
            "lllang": "en",
            "redirects": 1
        }
        data = call_wiki_api(WIKI_API_URL_VI, params)
        pages = data.get("query", {}).get("pages", {})
        for _, page in pages.items():
            langlinks = page.get("langlinks", [])
            if langlinks and isinstance(langlinks, list) and len(langlinks) > 0:
                item = langlinks[0]
                if item and isinstance(item, dict):
                    return item.get("*")
        return None
    except Exception as e:
        print(f"Error in lay_lien_ket_ngon_ngu ({title_vi}): {e}")
        return None

def lay_cac_lien_ket_trong_bai(url_api, title, main_topic_keywords=None):
    """
    Lấy danh sách các links trong bài viết.
    Chỉ lấy các link có liên quan đến từ khóa của chủ đề chính để tránh lạc đề.
    """
    try:
        params = {
            "action": "query",
            "format": "json",
            "prop": "links",
            "titles": title,
            "plnamespace": 0,
            "pllimit": 10, # Lấy nhiều hơn chút để lọc
            "redirects": 1
        }
        data = call_wiki_api(url_api, params)
        pages = data.get("query", {}).get("pages", {})
        links = []
        
        # Chuẩn bị từ khóa lọc
        keywords = []
        if main_topic_keywords:
            keywords = [k.lower() for k in main_topic_keywords.split() if len(k) > 3]
            
        for _, page in pages.items():
            plinks = page.get("links")
            if plinks and isinstance(plinks, list):
                for link in plinks:
                    if link and isinstance(link, dict):
                        t = link.get("title")
                        if t: 
                            # FILTERING LOGIC
                            if not keywords:
                                links.append(t)
                            else:
                                t_lower = t.lower()
                                # Chỉ lấy nếu title chứa ít nhất 1 từ khóa quan trọng của topic
                                if any(k in t_lower for k in keywords):
                                    links.append(t)
                                    
        return links[:3] # Chỉ lấy tối đa 3 link liên quan nhất
    except Exception as e:
        print(f"Error in lay_cac_lien_ket_trong_bai ({title}): {e}")
        return []

def tim_kiem_bai_viet_vi_du(url_api, topic):
    """Tìm bài viết chuyên về ví dụ hoặc ứng dụng của chủ đề"""
    try:
        query = f"{topic} examples applications case studies"
        title = tim_kiem_tieu_de(url_api, query)
        if title and title.lower() != topic.lower():
            print(f"  -> Tim thay bai viet vi du: {title}")
            content, _ = lay_noi_dung_va_anh(url_api, title, chars=2000)
            return content
        return ""
    except Exception as e:
        print(f"Error in tim_kiem_bai_viet_vi_du: {e}")
        return ""

def lay_lien_ket_ngoai(url_api, title, limit=5):
    """Lấy danh sách các liên kết ngoài (Tài liệu tham khảo)"""
    try:
        params = {
            "action": "query",
            "format": "json",
            "prop": "extlinks",
            "titles": title,
            "ellimit": limit,
            "redirects": 1
        }
        data = call_wiki_api(url_api, params)
        pages = data.get("query", {}).get("pages", {})
        links = []
        for _, page in pages.items():
            extlinks = page.get("extlinks", [])
            if extlinks:
                for item in extlinks:
                    url = item.get("*")
                    # Lọc URL rác, social media, file pdf...
                    if url and url.startswith("http"):
                        skip_domains = ["facebook.com", "twitter.com", "youtube.com", "instagram.com", "doi.org", "archive.org", "google.com"]
                        if not any(d in url for d in skip_domains) and not url.endswith(".pdf"):
                            links.append(url)
        return list(set(links))
    except Exception as e:
        print(f"Error in lay_lien_ket_ngoai: {e}")
        return []


def cao_noi_dung_url(url):
    """Cào nội dung text từ URL ngoài (đơn giản hoá)"""
    try:
        print(f"  -> Crawling external: {url}...")
        resp = requests.get(url, headers=HEADERS, timeout=10)
        if resp.status_code == 200:
            html = resp.text
            # Loại bỏ script, style
            html = re.sub(r'<script.*?>.*?</script>', '', html, flags=re.DOTALL)
            html = re.sub(r'<style.*?>.*?</style>', '', html, flags=re.DOTALL)
            html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
            
            # Lấy text
            text = re.sub(r'<[^>]+>', ' ', html)
            text = re.sub(r'\s+', ' ', text).strip()
            
            # Chỉ lấy nếu đủ dài
            if len(text) > 1000:
                return text[:3000] + "..." # Lấy 3000 ký tự đầu
    except Exception as e:
        print(f"Error crawling {url}: {e}")
    return ""


def lay_noi_dung_wikipedia(chu_de: str) -> dict:
    """
    Lấy dữ liệu tổng hợp
    """
    try:
        tong_hop_noi_dung = []
        tong_hop_anh = []
        noi_dung_vi_du = []
        
        print(f"Dang lay du lieu (Text + Images) cho: {chu_de}...")
        
        # 1. Thử lấy Tiếng Việt
        title_vi = tim_kiem_tieu_de(WIKI_API_URL_VI, chu_de)
        
        if title_vi:
            c_vi, i_vi = lay_noi_dung_va_anh(WIKI_API_URL_VI, title_vi)
            if c_vi: tong_hop_noi_dung.append(c_vi)
            if i_vi: tong_hop_anh.extend(i_vi)
            
            # 2. Lấy Tiếng Anh tương ứng
            title_en = lay_lien_ket_ngon_ngu(title_vi)
            if title_en:
                print(f"  -> Found EN topic: {title_en}")
                c_en, i_en = lay_noi_dung_va_anh(WIKI_API_URL_EN, title_en)
                if c_en: tong_hop_noi_dung.append(f"\n\n=== ENGLISH DATA ===\n{c_en}")
                if i_en: tong_hop_anh.extend(i_en)
                
                # 3. Tìm bài viết ví dụ
                ex_data = tim_kiem_bai_viet_vi_du(WIKI_API_URL_EN, title_en)
                if ex_data:
                    noi_dung_vi_du.append(ex_data)
                    
                # 4. Deep Search Related Links (Wiki Internal) - STRICTER
                # Chỉ lấy link liên quan đến tên topic gốc
                related_tieu_de = lay_cac_lien_ket_trong_bai(WIKI_API_URL_EN, title_en, main_topic_keywords=chu_de)
                for rt in related_tieu_de[:1]: # Chỉ lấy 1 related article tốt nhất
                     if isinstance(rt, str) and len(rt.split()) > 1:
                        c_rel, i_rel = lay_noi_dung_va_anh(WIKI_API_URL_EN, rt, chars=1500)
                        if c_rel: tong_hop_noi_dung.append(f"\n\n--- RELATED WIKI: {rt} ---\n{c_rel}")
                        if i_rel: tong_hop_anh.extend(i_rel)

                # 5. External Links Analysis (NEW)
                ext_links = lay_lien_ket_ngoai(WIKI_API_URL_EN, title_en, limit=3)
                for link in ext_links:
                    ext_content = cao_noi_dung_url(link)
                    if ext_content:
                        tong_hop_noi_dung.append(f"\n\n--- EXTERNAL REFERENCE ({link}) ---\n{ext_content}")

        else:
            # Fallback: Tìm trực tiếp tiếng Anh
            print("  -> Khong thay TV, tim truc tiep EN...")
            title_en = tim_kiem_tieu_de(WIKI_API_URL_EN, chu_de)
            if title_en:
                c_en, i_en = lay_noi_dung_va_anh(WIKI_API_URL_EN, title_en)
                if c_en: tong_hop_noi_dung.append(c_en)
                if i_en: tong_hop_anh.extend(i_en)
                
                ex_data = tim_kiem_bai_viet_vi_du(WIKI_API_URL_EN, title_en)
                if ex_data: noi_dung_vi_du.append(ex_data)
                
                # External links for fallback
                ext_links = lay_lien_ket_ngoai(WIKI_API_URL_EN, title_en, limit=3)
                for link in ext_links:
                    ext_content = cao_noi_dung_url(link)
                    if ext_content:
                        tong_hop_noi_dung.append(f"\n\n--- EXTERNAL REFERENCE ({link}) ---\n{ext_content}")

        return {
            "text": "\n\n".join(tong_hop_noi_dung),
            "images": list(set(tong_hop_anh)),
            "examples": "\n\n".join(noi_dung_vi_du)
        }
    except Exception as e:
        print(f"FATAL Error in lay_noi_dung_wikipedia: {e}")
        return {
            "text": "",
            "images": [],
            "examples": ""
        }
