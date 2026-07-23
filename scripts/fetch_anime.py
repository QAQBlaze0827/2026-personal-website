from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, urljoin, urlparse
from urllib.request import Request, urlopen
import json
import os
import re


BASE_URL = "https://ani.gamer.com.tw/"
GATHER_URL = urljoin(BASE_URL, "mygather.php")
ROOT_DIR = Path(__file__).resolve().parents[1]
ENV_PATH = ROOT_DIR / ".env"
OUTPUT_PATH = ROOT_DIR / "src" / "data" / "anime.json"
COVER_DIR = ROOT_DIR / "public" / "anime-covers"
START_PAGE = 1
END_PAGE = 5


def load_env(path: Path) -> None:
    # 讀取 .env，讓 Cookie 留在本機，不要寫死在程式碼裡。
    if not path.exists():
        return

    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()

        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")

        os.environ.setdefault(key, value)


def has_class(attrs: dict[str, str], class_name: str) -> bool:
    return class_name in attrs.get("class", "").split()


class AnimeGatherParser(HTMLParser):
    void_tags = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}

    def __init__(self) -> None:
        super().__init__()
        self.items: list[dict[str, str]] = []
        self.current_item: dict[str, str] | None = None
        self.current_depth = 0
        self.is_reading_title = False
        self.title_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs_list: list[tuple[str, str | None]]) -> None:
        attrs = {key: value or "" for key, value in attrs_list}

        # 每一筆收藏動畫外層是 <a class="theme-list-main">。
        if self.current_item is None and tag == "a" and has_class(attrs, "theme-list-main"):
            self.current_item = {
                "title": "",
                "image": "",
                "url": urljoin(BASE_URL, attrs.get("href", "")),
            }
            self.current_depth = 1
            return

        if self.current_item is None:
            return

        if tag not in self.void_tags:
            self.current_depth += 1

        # 圖片可能放在 data-src，也可能放在 src，所以兩個都檢查。
        if tag == "img" and has_class(attrs, "theme-img"):
            image_url = attrs.get("data-src") or attrs.get("src") or ""
            self.current_item["image"] = urljoin(BASE_URL, image_url)

            if not self.current_item["title"] and attrs.get("alt"):
                self.current_item["title"] = attrs["alt"].strip()

        # 動漫名稱在 <p class="theme-name"> 裡。
        if tag == "p" and has_class(attrs, "theme-name"):
            self.is_reading_title = True
            self.title_parts = []

    def handle_data(self, data: str) -> None:
        if self.is_reading_title:
            self.title_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if self.current_item is None:
            return

        if tag == "p" and self.is_reading_title:
            title = "".join(self.title_parts).strip()
            if title:
                self.current_item["title"] = title
            self.is_reading_title = False
            self.title_parts = []

        if tag not in self.void_tags:
            self.current_depth -= 1

        if self.current_depth == 0:
            if self.current_item["title"] and self.current_item["image"]:
                self.items.append(self.current_item)
            self.current_item = None


def fetch_gather_html(cookie: str, page: int) -> str:
    # page=1 到 page=5 分頁抓收藏清單。
    url = f"{GATHER_URL}?page={page}&sort=0"
    request = Request(
        url,
        headers={
            "Cookie": cookie,
            "User-Agent": "Mozilla/5.0",
        },
    )

    with urlopen(request, timeout=20) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace")


def get_anime_id(item: dict[str, str]) -> str:
    # 巴哈動畫頁網址會有 sn，可以拿來當穩定的圖片檔名。
    query = parse_qs(urlparse(item["url"]).query)
    sn = query.get("sn", [""])[0]

    if sn:
        return sn

    # 如果未來網址沒有 sn，就用名稱轉成簡單檔名當備案。
    return re.sub(r"[^0-9A-Za-z_-]+", "-", item["title"]).strip("-")


def get_image_extension(image_url: str) -> str:
    extension = Path(urlparse(image_url).path).suffix.lower()

    if extension in {".jpg", ".jpeg", ".png", ".webp"}:
        return extension

    return ".jpg"


def download_cover(item: dict[str, str], cookie: str) -> str:
    image_url = item["image"]
    file_name = f"{get_anime_id(item)}{get_image_extension(image_url)}"
    output_path = COVER_DIR / file_name

    # public 底下的檔案會直接變成網站根目錄路徑，例如 /anime-covers/xxx.jpg。
    public_path = f"/anime-covers/{file_name}"

    if output_path.exists():
        return public_path

    request = Request(
        image_url,
        headers={
            "Cookie": cookie,
            "Referer": GATHER_URL,
            "User-Agent": "Mozilla/5.0",
        },
    )

    with urlopen(request, timeout=20) as response:
        output_path.write_bytes(response.read())

    return public_path


def main() -> None:
    load_env(ENV_PATH)
    cookie = os.environ.get("BAHAMUT_COOKIE", "").strip()

    if not cookie:
        raise SystemExit("找不到 BAHAMUT_COOKIE，請先在 .env 加上 BAHAMUT_COOKIE=你的 Cookie")

    COVER_DIR.mkdir(parents=True, exist_ok=True)

    items: list[dict[str, str]] = []
    seen_keys: set[str] = set()

    for page in range(START_PAGE, END_PAGE + 1):
        html = fetch_gather_html(cookie, page)
        parser = AnimeGatherParser()
        parser.feed(html)

        for item in parser.items:
            key = item.get("url") or item["title"]
            if key in seen_keys:
                continue

            seen_keys.add(key)
            items.append(item)

        print(f"第 {page} 頁解析到 {len(parser.items)} 筆")

    for item in items:
        original_image = item["image"]
        item["sourceImage"] = original_image

        # 單張圖片失敗不應該讓整個爬蟲中斷，先保留原始圖片網址當備案。
        try:
            item["image"] = download_cover(item, cookie)
        except Exception as error:
            print(f"下載圖片失敗：{item['title']}，原因：{error}")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(items, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"已輸出 {len(items)} 筆動漫資料到 {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
