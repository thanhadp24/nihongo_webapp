import html
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


INDEX_URL = "https://www.vnjpclub.com/somatome-n2-han-tu/"
OUTPUT = Path("database/import/jlpt_n2_kanji_by_topic_db_import.json")
KANJI_API_CACHE = Path("tmp/cache/kanjiapi_n2.json")
ENRICH_KANJI_API = os.environ.get("ENRICH_KANJI_API") == "1"


WEEKS = {
    1: {"title": "みる①", "title_vi": "Nhìn/nhận biết 1", "page_start": 11},
    2: {"title": "つかう①", "title_vi": "Sử dụng 1", "page_start": 27},
    3: {"title": "よむ①", "title_vi": "Đọc 1", "page_start": 43},
    4: {"title": "かく", "title_vi": "Viết", "page_start": 59},
    5: {"title": "つかう②", "title_vi": "Sử dụng 2", "page_start": 75},
    6: {"title": "みる②", "title_vi": "Nhìn/nhận biết 2", "page_start": 91},
    7: {"title": "よむ②", "title_vi": "Đọc 2", "page_start": 107},
    8: {"title": "しる", "title_vi": "Biết/hiểu thông tin", "page_start": 123},
}


TOPIC_NAME_VI = {
    (1, 1): "Biển báo và chú ý",
    (1, 2): "Biển chỉ dẫn thường thấy trong tòa nhà",
    (1, 3): "Biển chỉ dẫn thường thấy trong tòa nhà 2",
    (1, 4): "Biển chỉ dẫn thường thấy ở ga",
    (1, 5): "Biển chỉ dẫn thường thấy trên phương tiện",
    (1, 6): "Biển chỉ dẫn thường thấy ở bưu điện và bệnh viện",
    (2, 1): "Máy bán vé tự động",
    (2, 2): "Máy rút/trả tiền tự động",
    (2, 3): "Máy bán hàng tự động và máy bán vé",
    (2, 4): "Điều khiển đồ điện gia dụng",
    (2, 5): "Điện thoại và điện thoại di động",
    (2, 6): "Điện thoại di động và máy tính",
    (3, 1): "Thông báo phí và giấy chuyển khoản",
    (3, 2): "Thông báo vắng nhà",
    (3, 3): "Thẻ tích điểm, phiếu quà tặng và phiếu gửi đồ giặt",
    (3, 4): "Phân loại rác",
    (3, 5): "Các loại thông báo 1",
    (3, 6): "Các loại thông báo 2",
    (4, 1): "Phiếu truyền đạt và đơn đăng ký",
    (4, 2): "Viết trả lời",
    (4, 3): "Email và bưu thiếp",
    (4, 4): "Email công việc",
    (4, 5): "Phiếu/trang trả lời",
    (4, 6): "Bài văn",
    (5, 1): "Đồ gia dụng: bình nước và máy sưởi",
    (5, 2): "Đồ gia dụng: chất tẩy rửa 1",
    (5, 3): "Đồ gia dụng: chất tẩy rửa 2",
    (5, 4): "Đồ gia dụng: thuốc",
    (5, 5): "Thực phẩm",
    (5, 6): "Chuông cửa có hình và máy tính",
    (6, 1): "Quảng cáo và tờ rơi",
    (6, 2): "Tờ quảng cáo kẹp trong báo",
    (6, 3): "Quảng cáo",
    (6, 4): "Bản đồ",
    (6, 5): "Di sản văn hóa và trưng bày",
    (6, 6): "Cái nào?",
    (7, 1): "Tuyển dụng và tuyển mộ",
    (7, 2): "Bảng thông báo và báo địa phương",
    (7, 3): "Thực đơn và nhãn thành phần",
    (7, 4): "Hướng dẫn dự thi",
    (7, 5): "Thông tin giao thông",
    (7, 6): "Thông tin thời tiết",
    (8, 1): "Tin nhanh",
    (8, 2): "Tiêu đề 1",
    (8, 3): "Tiêu đề 2",
    (8, 4): "Bài báo 1",
    (8, 5): "Bài báo 2",
    (8, 6): "Bài báo 3",
}


TOPIC_NAME_READING = {
    (1, 1): "たてふだ・ちゅういがき",
    (1, 2): "たてもののなかでよくみるひょうじ",
    (1, 3): "たてもののなかでよくみるひょうじに",
    (1, 4): "えきでよくみるひょうじ",
    (1, 5): "のりものでよくみるひょうじ",
    (1, 6): "ゆうびんきょく・びょういんでよくみるひょうじ",
    (2, 1): "じどうけんばいき",
    (2, 2): "げんきんじどうしはらいき",
    (2, 3): "じどうはんばいき・じどうけんばいき",
    (2, 4): "かでんのりもこん",
    (2, 5): "でんわ・けいたいでんわ",
    (2, 6): "けいたいでんわ・ぱそこん",
    (3, 1): "りょうきんつうち・ふりこみようし",
    (3, 2): "ふざいつうち",
    (3, 3): "ぽいんとかーど・しょうひんけん・くりーにんぐあずかりひょう",
    (3, 4): "ごみのぶんべつ",
    (3, 5): "いろいろなつうちいち",
    (3, 6): "いろいろなつうちに",
    (4, 1): "でんぴょう・もうしこみしょ",
    (4, 2): "へんじをかく",
    (4, 3): "めーる・はがき",
    (4, 4): "びじねすめーる",
    (4, 5): "とうあんようし",
    (4, 6): "さくぶん",
    (5, 1): "かていようひん・ぽっと・ひーたー",
    (5, 2): "かていようひん・せんざいいち",
    (5, 3): "かていようひん・せんざいに",
    (5, 4): "かていようひん・くすり",
    (5, 5): "しょくひん",
    (5, 6): "いんたーほん・ぱそこん",
    (6, 1): "こうこく・ちらし",
    (6, 2): "おりこみこうこく",
    (6, 3): "こうこく",
    (6, 4): "ちず",
    (6, 5): "ぶんかざい・てんじ",
    (6, 6): "どっち",
    (7, 1): "きゅうじん・ぼしゅう",
    (7, 2): "けいじばん・ちいきしんぶん",
    (7, 3): "めにゅー・せいぶんひょうじ",
    (7, 4): "じゅけんあんない",
    (7, 5): "こうつうじょうほう",
    (7, 6): "きしょうじょうほう",
    (8, 1): "そくほう",
    (8, 2): "みだしいち",
    (8, 3): "みだしに",
    (8, 4): "きじいち",
    (8, 5): "きじに",
    (8, 6): "きじさん",
}


KANJI_RE = re.compile(r"[\u3400-\u9fff]")
LINK_RE = re.compile(r"第(\d+)週\s*\((\d+)\)\s*[–-]\s*(.+)")
POST_RE = re.compile(r"wp-json/wp/v2/posts/(\d+)")


def request_text(url: str) -> str:
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=45)
    response.raise_for_status()
    return response.text


def text_clean(value: str) -> str:
    value = html.unescape(value or "")
    value = value.replace("\xa0", " ")
    value = value.replace("\u3000", " ")
    value = value.replace("／", "/")
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def kanji_only(value: str) -> str:
    return "".join(KANJI_RE.findall(value))


def normalize_han_viet(value: str) -> str:
    return text_clean(value).lower()


def extract_topic_links() -> list[dict]:
    soup = BeautifulSoup(request_text(INDEX_URL), "html.parser")
    topics = []
    seen = set()

    for anchor in soup.find_all("a", href=True):
        href = urljoin(INDEX_URL, anchor["href"])
        label = text_clean(anchor.get_text(" ", strip=True))
        match = LINK_RE.search(label)
        if not match:
            continue

        week = int(match.group(1))
        day = int(match.group(2))
        if day == 7:
            continue
        if not (1 <= week <= 8 and 1 <= day <= 6):
            continue

        key = (week, day)
        if key in seen:
            continue
        seen.add(key)

        topics.append(
            {
                "week": week,
                "day": day,
                "name": text_clean(match.group(3)),
                "name_vi": TOPIC_NAME_VI[key],
                "url": href,
            }
        )

    topics.sort(key=lambda item: (item["week"], item["day"]))
    return topics


def fetch_post_content(url: str) -> str:
    page_html = request_text(url)
    post_match = POST_RE.search(page_html)
    if not post_match:
        raise ValueError(f"Cannot find WP REST post id for {url}")

    rest_url = f"https://www.vnjpclub.com/wp-json/wp/v2/posts/{post_match.group(1)}"
    post = requests.get(rest_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=45)
    post.raise_for_status()
    return post.json()["content"]["rendered"]


def load_kanji_api_cache() -> dict:
    if KANJI_API_CACHE.exists():
        return json.loads(KANJI_API_CACHE.read_text(encoding="utf-8"))
    return {}


def save_kanji_api_cache(cache: dict) -> None:
    KANJI_API_CACHE.parent.mkdir(parents=True, exist_ok=True)
    KANJI_API_CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def fetch_kanji_api(character: str, cache: dict) -> dict:
    if not ENRICH_KANJI_API:
        return {}

    if character in cache:
        return cache[character]

    response = requests.get(
        f"https://kanjiapi.dev/v1/kanji/{character}",
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=30,
    )
    if response.status_code == 404:
        cache[character] = {}
        return cache[character]

    response.raise_for_status()
    cache[character] = response.json()
    return cache[character]


def join_readings(values: list[str] | None) -> str | None:
    if not values:
        return None
    return "、".join(values)


def extract_kanji_entries(content_html: str) -> list[dict]:
    soup = BeautifulSoup(content_html, "html.parser")
    table = soup.select_one("#tab3 table")
    if table is None:
        raise ValueError("Cannot find kanji table #tab3 table")

    entries = []
    current = None

    for row in table.find_all("tr"):
        cells = [text_clean(cell.get_text(" ", strip=True)) for cell in row.find_all(["td", "th"])]
        if len(cells) < 4 or cells[0] == "Chữ Hán":
            continue

        first, han_viet, reading, meaning = cells[:4]
        chars = kanji_only(first)
        is_header = len(chars) == 1 and not text_clean(meaning)

        if is_header:
            current = {
                "character_value": chars,
                "han_viet": normalize_han_viet(han_viet),
                "source_reading": text_clean(reading),
                "meaning_vi": normalize_han_viet(han_viet),
                "words": [],
            }
            entries.append(current)
            continue

        if current is None:
            continue

        word = text_clean(first)
        if not word or not kanji_only(word):
            continue

        current["words"].append(
            {
                "word": word,
                "source_han_viet": text_clean(han_viet),
                "reading": text_clean(reading),
                "meaning_vi": text_clean(meaning) or normalize_han_viet(han_viet),
            }
        )

    return entries


def merge_duplicate_entries(entries: list[dict]) -> list[dict]:
    merged = []
    by_character = {}

    for entry in entries:
        character = entry["character_value"]
        existing = by_character.get(character)
        if existing is None:
            by_character[character] = entry
            merged.append(entry)
            continue

        existing["words"].extend(entry["words"])
        if entry.get("source_reading") and entry["source_reading"] not in existing.get("source_reading", ""):
            existing["source_reading"] = text_clean(
                f"{existing.get('source_reading') or ''}/{entry['source_reading']}"
            )

    return merged


def build_word_example(word: str, reading: str, meaning_vi: str) -> tuple[str, str, str]:
    return (
        f"この文で「{word}」を確認します。",
        f"このぶんで「{reading}」をかくにんします。",
        f"Tôi kiểm tra từ '{word}' ({meaning_vi}) trong câu này.",
    )


def build_data() -> dict:
    source_topics = extract_topic_links()
    if len(source_topics) != 48:
        raise ValueError(f"Expected 48 source topics, got {len(source_topics)}")

    topics = []
    characters = []
    words = []
    character_id = 1
    word_id = 1
    kanji_cache = load_kanji_api_cache()

    for topic_id, source_topic in enumerate(source_topics, start=1):
        week = source_topic["week"]
        day = source_topic["day"]
        week_meta = WEEKS[week]
        topics.append(
            {
                "id": topic_id,
                "jlpt_level_id": 4,
                "name": source_topic["name"],
                "name_reading": TOPIC_NAME_READING.get((week, day)),
                "name_vi": source_topic["name_vi"],
                "description": (
                    f"Soumatome N2 Kanji - Week {week} Day {day}: "
                    f"{source_topic['name']} ({source_topic['name_vi']})."
                ),
                "source_book": "Soumatome N2 Kanji",
                "source_week": week,
                "source_week_title": week_meta["title"],
                "source_week_title_vi": week_meta["title_vi"],
                "source_day": day,
                "source_page_start": week_meta["page_start"] + ((day - 1) * 2),
                "source_url": source_topic["url"],
                "display_order": topic_id,
                "is_published": True,
                "version": 1,
            }
        )

        entries = merge_duplicate_entries(extract_kanji_entries(fetch_post_content(source_topic["url"])))
        if not entries:
            raise ValueError(f"No kanji entries for {source_topic['url']}")

        for character_order, entry in enumerate(entries, start=1):
            api_data = fetch_kanji_api(entry["character_value"], kanji_cache)
            characters.append(
                {
                    "id": character_id,
                    "kanji_topic_id": topic_id,
                    "character_value": entry["character_value"],
                    "han_viet": entry["han_viet"],
                    "onyomi": join_readings(api_data.get("on_readings")) or entry["source_reading"] or None,
                    "kunyomi": join_readings(api_data.get("kun_readings")),
                    "meaning_vi": entry["meaning_vi"],
                    "stroke_count": api_data.get("stroke_count"),
                    "mnemonic_vi": None,
                    "display_order": character_order,
                    "is_published": True,
                    "version": 1,
                }
            )

            for word_order, source_word in enumerate(entry["words"], start=1):
                example_sentence, example_reading, example_meaning = build_word_example(
                    source_word["word"],
                    source_word["reading"],
                    source_word["meaning_vi"],
                )
                words.append(
                    {
                        "id": word_id,
                        "kanji_character_id": character_id,
                        "word": source_word["word"],
                        "reading": source_word["reading"],
                        "meaning_vi": source_word["meaning_vi"],
                        "example_sentence": example_sentence,
                        "example_reading": example_reading,
                        "example_meaning_vi": example_meaning,
                        "display_order": word_order,
                        "is_published": True,
                        "version": 1,
                    }
                )
                word_id += 1

            character_id += 1

    if ENRICH_KANJI_API:
        save_kanji_api_cache(kanji_cache)
    return {
        "metadata": {
            "name": "JLPT N2 kanji import data by Soumatome topic",
            "status": "ready_for_review_database_import",
            "jlpt_level_code": "N2",
            "jlpt_level_id_assumption": 4,
            "source_url": INDEX_URL,
            "source_file": "plan/kanji/Soumatome N2 Kanji (ebook).pdf",
            "source_note": (
                "Topic list and kanji/vocabulary rows were extracted from VNJPCLUB WordPress REST "
                "content for Somatome N2 Kanji. The local ebook PDF is scan-based with no text layer. "
                "KanjiAPI enrichment is optional; run with ENRICH_KANJI_API=1 to supplement "
                "stroke counts and separated on/kun readings."
            ),
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "notes": [
                "kanji_topics.name is Japanese-first; kanji_topics.name_vi is the Vietnamese subtitle.",
                "No note field is generated for kanji_characters.",
                "Without ENRICH_KANJI_API=1, source readings are stored in onyomi, kunyomi is null, and stroke_count is null.",
                "example_* fields are generated learning examples for every kanji word.",
            ],
            "import_order_when_completed": [
                "kanji_topics",
                "kanji_characters",
                "kanji_words",
            ],
        },
        "kanji_topics": topics,
        "kanji_characters": characters,
        "kanji_words": words,
    }


def validate(data: dict) -> None:
    if len(data["kanji_topics"]) != 48:
        raise ValueError(f"Expected 48 topics, got {len(data['kanji_topics'])}")

    topic_ids = {topic["id"] for topic in data["kanji_topics"]}
    character_ids = {char["id"] for char in data["kanji_characters"]}
    seen_topic_orders = set()
    seen_character_topic_orders = set()
    seen_word_orders = set()

    for topic in data["kanji_topics"]:
        for key in ("id", "jlpt_level_id", "name", "name_vi", "source_week", "source_day", "display_order"):
            if topic.get(key) in (None, ""):
                raise ValueError(f"Missing {key} in topic {topic}")
        if topic["display_order"] in seen_topic_orders:
            raise ValueError(f"Duplicate topic display_order {topic['display_order']}")
        seen_topic_orders.add(topic["display_order"])

    for char in data["kanji_characters"]:
        if char["kanji_topic_id"] not in topic_ids:
            raise ValueError(f"Missing topic for kanji {char['character_value']}")
        for key in ("character_value", "han_viet", "meaning_vi", "display_order"):
            if char.get(key) in (None, ""):
                raise ValueError(f"Missing {key} for kanji {char['character_value']}")
        if "note" in char:
            raise ValueError(f"Unexpected note field for kanji {char['character_value']}")
        key = (char["kanji_topic_id"], char["display_order"])
        if key in seen_character_topic_orders:
            raise ValueError(f"Duplicate kanji order in topic: {key}")
        seen_character_topic_orders.add(key)

    for word in data["kanji_words"]:
        if word["kanji_character_id"] not in character_ids:
            raise ValueError(f"Missing kanji for word {word['word']}")
        for key in (
            "word",
            "reading",
            "meaning_vi",
            "example_sentence",
            "example_reading",
            "example_meaning_vi",
            "display_order",
        ):
            if word.get(key) in (None, ""):
                raise ValueError(f"Missing {key} for word id={word['id']}")
        key = (word["kanji_character_id"], word["display_order"])
        if key in seen_word_orders:
            raise ValueError(f"Duplicate word order under kanji: {key}")
        seen_word_orders.add(key)

    empty_topics = [
        topic["id"]
        for topic in data["kanji_topics"]
        if not any(char["kanji_topic_id"] == topic["id"] for char in data["kanji_characters"])
    ]
    if empty_topics:
        raise ValueError(f"Topics without kanji: {empty_topics}")


if __name__ == "__main__":
    data = build_data()
    validate(data)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT}")
    print(f"topics={len(data['kanji_topics'])}")
    print(f"kanji_characters={len(data['kanji_characters'])}")
    print(f"kanji_words={len(data['kanji_words'])}")
