import html
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


INDEX_URL = "https://www.vnjpclub.com/somatome-n3-han-tu/"
OUTPUT = Path("database/import/jlpt_n3_kanji_by_topic_db_import.json")


WEEKS = {
    1: {"title": "でかける①", "title_vi": "Đi ra ngoài 1", "page_start": 11},
    2: {"title": "でかける②", "title_vi": "Đi ra ngoài 2", "page_start": 27},
    3: {"title": "つかう", "title_vi": "Sử dụng", "page_start": 43},
    4: {"title": "かう", "title_vi": "Mua sắm", "page_start": 59},
    5: {"title": "かく", "title_vi": "Viết", "page_start": 75},
    6: {"title": "よむ", "title_vi": "Đọc", "page_start": 91},
}


TOPIC_NAME_VI = {
    (1, 1): "Bãi đỗ xe",
    (1, 2): "Vạch qua đường",
    (1, 3): "Biển báo",
    (1, 4): "Sân ga",
    (1, 5): "Tàu tốc hành",
    (1, 6): "Xe buýt",
    (2, 1): "Nhà hàng",
    (2, 2): "Cấm hút thuốc",
    (2, 3): "Bản đồ du lịch",
    (2, 4): "Bản đồ thị trấn",
    (2, 5): "Bệnh viện",
    (2, 6): "Khi gặp rắc rối",
    (3, 1): "Cần giữ lạnh",
    (3, 2): "Hạn sử dụng ngon nhất",
    (3, 3): "Máy bán hàng tự động",
    (3, 4): "Công thức nấu ăn",
    (3, 5): "Máy photocopy và điện thoại trả lời tự động",
    (3, 6): "Điện thoại di động",
    (4, 1): "Đồ dùng hằng ngày",
    (4, 2): "Email quảng cáo",
    (4, 3): "Bán hàng qua mạng",
    (4, 4): "Đơn đăng ký",
    (4, 5): "Đặt hàng",
    (4, 6): "Thông báo vắng nhà",
    (5, 1): "Gửi email",
    (5, 2): "Khảo sát",
    (5, 3): "Lớp tiếng Nhật",
    (5, 4): "Viết bài văn",
    (5, 5): "Phiếu khám - nha khoa",
    (5, 6): "Phiếu khám - khám sức khỏe",
    (6, 1): "Thông tin thời tiết",
    (6, 2): "Tin tuyển dụng",
    (6, 3): "Bài báo thể thao",
    (6, 4): "Kinh tế",
    (6, 5): "Nóng lên toàn cầu",
    (6, 6): "Chính trị",
}

TOPIC_NAME_READING = {
    (1, 1): "ちゅうしゃじょう",
    (1, 2): "おうだんほどう",
    (1, 3): "さいん",
    (1, 4): "えきのほーむ",
    (1, 5): "とっきゅうでんしゃ",
    (1, 6): "ばす",
    (2, 1): "れすとらん",
    (2, 2): "きんえん",
    (2, 3): "かんこうちず",
    (2, 4): "まちのちず",
    (2, 5): "びょういん",
    (2, 6): "こまったときは",
    (3, 1): "ようれいぞう",
    (3, 2): "しょうみきげん",
    (3, 3): "じどうはんばいき",
    (3, 4): "れしぴ",
    (3, 5): "こぴーき・るすばんでんわ",
    (3, 6): "けいたいでんわ",
    (4, 1): "にちようひん",
    (4, 2): "こうこくめーる",
    (4, 3): "つうしんはんばい",
    (4, 4): "もうしこみしょ",
    (4, 5): "ちゅうもん",
    (4, 6): "ふざいつうち",
    (5, 1): "めーるをおくる",
    (5, 2): "あんけーと",
    (5, 3): "にほんごくらす",
    (5, 4): "かくさくぶん",
    (5, 5): "もんしんひょう・しかで",
    (5, 6): "もんしんひょう・けんこうしんだん",
    (6, 1): "てんきじょうほう",
    (6, 2): "きゅうじんこうこく",
    (6, 3): "すぽーつきじ",
    (6, 4): "けいざい",
    (6, 5): "ちきゅうおんだんか",
    (6, 6): "せいじ",
}


KANJI_RE = re.compile(r"[\u3400-\u9fff]")
LINK_RE = re.compile(r"第(\d+)週\s*\((\d+)\)\s*[–-]\s*(.+)")
POST_RE = re.compile(r"wp-json/wp/v2/posts/(\d+)")
KANJI_API_CACHE = Path("tmp/cache/kanjiapi_n3.json")


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
    value = text_clean(value)
    value = re.sub(r"\s+", " ", value)
    return value.lower()


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
        if not (1 <= week <= 6 and 1 <= day <= 6):
            continue

        key = (week, day)
        if key in seen:
            continue
        seen.add(key)

        name = text_clean(match.group(3))
        topics.append(
            {
                "week": week,
                "day": day,
                "name": name,
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
    data = post.json()
    return data["content"]["rendered"]


def load_kanji_api_cache() -> dict:
    if KANJI_API_CACHE.exists():
        return json.loads(KANJI_API_CACHE.read_text(encoding="utf-8"))
    return {}


def save_kanji_api_cache(cache: dict) -> None:
    KANJI_API_CACHE.parent.mkdir(parents=True, exist_ok=True)
    KANJI_API_CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def fetch_kanji_api(character: str, cache: dict) -> dict:
    if character in cache:
        return cache[character]

    url = f"https://kanjiapi.dev/v1/kanji/{character}"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
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
        strong = row.find("strong")
        is_kanji_header = strong is not None and bool(kanji_only(first))

        if is_kanji_header:
            chars = kanji_only(first)
            if not chars:
                continue
            current = {
                "character_value": chars[0],
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
    if len(source_topics) != 36:
        raise ValueError(f"Expected 36 source topics, got {len(source_topics)}")

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
                "jlpt_level_id": 3,
                "name": source_topic["name"],
                "name_reading": TOPIC_NAME_READING.get((week, day)),
                "name_vi": source_topic["name_vi"],
                "description": (
                    f"Soumatome N3 Kanji - Week {week} Day {day}: "
                    f"{source_topic['name']} ({source_topic['name_vi']})."
                ),
                "source_book": "Soumatome N3 Kanji",
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

        content_html = fetch_post_content(source_topic["url"])
        entries = merge_duplicate_entries(extract_kanji_entries(content_html))
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

    data = {
        "metadata": {
            "name": "JLPT N3 kanji import data by Soumatome topic",
            "status": "ready_for_review_database_import",
            "jlpt_level_code": "N3",
            "jlpt_level_id_assumption": 3,
            "source_url": INDEX_URL,
            "source_file": "plan/kanji/[VTI Mirai Share] 141 - Soumatome N3 Kanji.pdf",
            "source_note": (
                "Topic list and kanji/vocabulary rows were extracted from VNJPCLUB WordPress REST "
                "content for Somatome N3 Kanji. The local PDF is scan-based with no text layer. "
                "Stroke counts and separated on/kun readings were supplemented from KanjiAPI."
            ),
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "notes": [
                "Week 6 Day 6 is 政治, not 日記.",
                "kanji_topics.name is Japanese-first; kanji_topics.name_vi is the Vietnamese subtitle.",
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
    save_kanji_api_cache(kanji_cache)
    return data


def validate(data: dict) -> None:
    if len(data["kanji_topics"]) != 36:
        raise ValueError(f"Expected 36 topics, got {len(data['kanji_topics'])}")

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
