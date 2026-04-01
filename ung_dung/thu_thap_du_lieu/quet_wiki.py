import requests

WIKI_API_URL = "https://vi.wikipedia.org/w/api.php"

headers = {
    "User-Agent": "HeThongGiaoTrinhAI/1.0 (https://example.com; email@example.com)"
}


def tim_tieu_de_wikipedia(chu_de: str) -> str:
    """Tìm tiêu đề Wikipedia phù hợp nhất"""
    params = {
        "action": "query",
        "list": "search",
        "srsearch": chu_de,
        "format": "json",
        "utf8": 1,
        "origin": "*"
    }

    response = requests.get(WIKI_API_URL, params=params, headers=headers, timeout=15)
    if response.status_code != 200:
        return ""

    data = response.json()
    ket_qua = data.get("query", {}).get("search", [])

    if not ket_qua:
        return ""

    return ket_qua[0]["title"]


def lay_noi_dung_wikipedia(chu_de: str) -> str:
    """Lấy nội dung bài Wikipedia đầy đủ"""

    tieu_de = tim_tieu_de_wikipedia(chu_de)
    if not tieu_de:
        return ""

    params = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "explaintext": True,
        "titles": tieu_de,
        "redirects": 1,
        "origin": "*"
    }

    response = requests.get(
        WIKI_API_URL,
        params=params,
        headers=headers,
        timeout=15
    )

    if response.status_code != 200:
        return ""

    data = response.json()
    pages = data.get("query", {}).get("pages", {})

    for _, page in pages.items():
        noi_dung = page.get("extract", "")
        if noi_dung and len(noi_dung) > 300:
            return noi_dung

    return ""
