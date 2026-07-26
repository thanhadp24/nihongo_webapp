import json
import re
from pathlib import Path

import fitz


JLPT_LEVEL_ID = 2
GRAMMAR_CHAPTER_START_ID = 1
GRAMMAR_LESSON_START_ID = 120
GRAMMAR_EXAMPLE_START_ID = 154

PLAN_DIR = Path("plan")
OUTPUT_JSON_PATH = Path("database/import/jlpt_n4_grammar_by_chapter_db_import.json")
OUTPUT_SQL_PATH = Path("database/seed/008_jlpt_n4_grammar.sql")


def find_n4_grammar_folder() -> Path:
    for path in PLAN_DIR.iterdir():
        if path.is_dir() and "n4" in path.name.lower():
            return path
    raise FileNotFoundError("Could not find plan folder containing N4 grammar PDFs")


def chapter_number_from_name(path: Path) -> int:
    match = re.search(r"bài\s+(\d+)", path.name, flags=re.IGNORECASE)
    if not match:
        raise ValueError(f"Could not read chapter number from {path.name}")
    return int(match.group(1))


def extract_lines(path: Path) -> list[str]:
    doc = fitz.open(path)
    lines: list[str] = []
    for page in doc:
        for line in page.get_text().splitlines():
            line = clean_line(line)
            if line:
                lines.append(line)
    return lines


def clean_line(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def is_upper_toc_title(value: str) -> bool:
    letters = [ch for ch in value if ch.isalpha()]
    if not letters:
        return False
    upper_letters = [ch for ch in letters if ch.upper() == ch and ch.lower() != ch]
    return len(upper_letters) / max(len(letters), 1) > 0.7


def is_noise_line(value: str) -> bool:
    if not value:
        return True
    if value in {"［", "］", "[", "]", "|"}:
        return True
    if value.startswith("NGỮ PHÁP BÀI"):
        return True
    if re.fullmatch(r"[・•Ø➢\[\]＋+~～／/|]+", value):
        return True
    return False


def is_heading_candidate(lines: list[str], index: int) -> bool:
    line = lines[index]
    if re.match(r"^\d+\.\s*.+", line):
        return True
    if re.fullmatch(r"\d+\.", line):
        return True
    return False


def heading_number_and_title(lines: list[str], index: int) -> tuple[int, str]:
    line = lines[index]
    match = re.match(r"^(\d+)\.\s*(.+)?$", line)
    if not match:
        raise ValueError(f"Not a heading line: {line}")
    number = int(match.group(1))
    title = clean_line(match.group(2) or "")
    if title:
        return number, normalize_title(title)

    title_parts: list[str] = []
    for next_line in lines[index + 1 : min(index + 8, len(lines))]:
        if is_noise_line(next_line):
            continue
        if looks_like_pattern(next_line) and title_parts:
            break
        title_parts.append(next_line)
        if title_parts and (next_line.endswith(":") or next_line.endswith("：")):
            break
        if len(title_parts) >= 2:
            break
    return number, normalize_title(" ".join(title_parts))


def normalize_title(value: str) -> str:
    value = value.replace("HH", "").replace("H  ", " ")
    value = re.sub(r"\s+", " ", value)
    value = re.sub(r"^\s*[\[］\]]+\s*", "", value)
    value = value.strip(" .")
    return value[:255]


def title_score(title: str) -> int:
    score = 0
    if title:
        score += 5
    if not is_upper_toc_title(title):
        score += 5
    if ":" in title or "：" in title:
        score += 2
    if any(ch in title for ch in "∼～?？"):
        score += 1
    if len(title) > 70:
        score -= 4
    if re.search(r"\b[1-9]\.|\bNGỮ PHÁP\b", title):
        score -= 5
    return score


def pick_headings(lines: list[str]) -> list[dict]:
    candidates: list[dict] = []
    for index, line in enumerate(lines):
        if not is_heading_candidate(lines, index):
            continue
        number, title = heading_number_and_title(lines, index)
        if number <= 0 or number > 30 or not title:
            continue
        candidates.append({"number": number, "title": title, "index": index, "score": title_score(title)})

    selected: dict[int, dict] = {}
    for candidate in candidates:
        number = candidate["number"]
        current = selected.get(number)
        if current is None or (candidate["score"], candidate["index"]) > (current["score"], current["index"]):
            selected[number] = candidate

    return [selected[number] for number in sorted(selected)]


def has_japanese(value: str) -> bool:
    return bool(re.search(r"[\u3040-\u30ff\u3400-\u9fff]", value))


def looks_like_pattern(value: str) -> bool:
    if is_noise_line(value):
        return False
    if has_japanese(value):
        return True
    return bool(re.search(r"\b[SVNAQ]\b|V\s*(ます|て|ない|る|た)|N\d?|A\s*(い|な)", value))


def looks_like_vietnamese(value: str) -> bool:
    if has_japanese(value):
        return False
    return bool(re.search(r"[A-Za-zÀ-ỹ]", value))


def lesson_body(lines: list[str], heading: dict, next_heading_index: int | None) -> list[str]:
    start = heading["index"]
    end = next_heading_index if next_heading_index is not None else len(lines)
    body = [line for line in lines[start:end] if not is_noise_line(line)]
    return body[:120]


def extract_pattern(title: str, body: list[str]) -> str:
    pattern_candidates: list[str] = []
    for line in body[:18]:
        if line.startswith("VD") or line.startswith("Cách dùng") or line.startswith("Ý nghĩa"):
            if line.startswith("VD"):
                break
            continue
        if re.match(r"^\d+\.", line):
            continue
        if looks_like_pattern(line) and not looks_like_example_sentence(line):
            pattern_candidates.append(line)
        if len(pattern_candidates) >= 2:
            break
    if pattern_candidates:
        return " / ".join(pattern_candidates)[:255]
    return title[:255]


def extract_explanation(title: str, body: list[str]) -> str:
    explanation_lines: list[str] = []
    capture = False
    for line in body:
        if line.startswith(("Cách dùng", "Ý nghĩa", "Chú ý", "Định nghĩa")):
            capture = True
            explanation_lines.append(line)
            continue
        if line.startswith("VD"):
            if explanation_lines:
                break
            capture = True
            continue
        if capture and looks_like_vietnamese(line):
            if re.match(r"^(Q|A)[:：]", line):
                continue
            explanation_lines.append(line)
        if len(" ".join(explanation_lines)) > 450:
            break

    if not explanation_lines:
        for line in body:
            if looks_like_vietnamese(line) and not re.match(r"^\d+\.", line):
                explanation_lines.append(line)
            if len(explanation_lines) >= 3:
                break

    text = " ".join(explanation_lines)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:900] if text else f"Mẫu ngữ pháp N4: {title}."


def extract_formation(pattern: str, body: list[str]) -> str:
    formation_lines: list[str] = []
    for line in body[:24]:
        if line.startswith(("VD", "Cách dùng", "Ý nghĩa", "Chú ý")):
            continue
        if looks_like_pattern(line):
            formation_lines.append(line)
        if len(formation_lines) >= 3:
            break
    return " / ".join(formation_lines)[:900] if formation_lines else pattern


def clean_translation_lines(lines: list[str]) -> str:
    text = " ".join(line for line in lines if looks_like_vietnamese(line))
    text = re.sub(r"\s+", " ", text).strip()
    text = re.split(r"\s*[❖Ø]\s*|\s+Q[:：]|\s+A[:：]", text, maxsplit=1)[0].strip()
    if len(text) > 220:
        clipped = text[:220]
        last_stop = max(clipped.rfind("."), clipped.rfind("?"), clipped.rfind("!"))
        if last_stop > 40:
            clipped = clipped[: last_stop + 1]
        text = clipped
    return text


def extract_examples(body: list[str], lesson_title: str, pattern: str) -> list[dict]:
    examples: list[dict] = []
    in_examples = False
    current_japanese: str | None = None
    current_vi: list[str] = []

    def flush():
        nonlocal current_japanese, current_vi
        if current_japanese and len(current_japanese) <= 140:
            meaning = clean_translation_lines(current_vi)
            if meaning:
                examples.append(
                    {
                        "japanese_text": current_japanese,
                        "reading": None,
                        "meaning_vi": meaning,
                    }
                )
        current_japanese = None
        current_vi = []

    for line in body:
        if line.startswith("VD"):
            in_examples = True
            continue
        if not in_examples and len(examples) == 0:
            continue
        if re.match(r"^\d+\.", line):
            continue
        if is_clean_japanese_example(line):
            flush()
            current_japanese = line
            current_vi = []
            continue
        if current_japanese and looks_like_vietnamese(line):
            current_vi.append(line)
        if len(examples) >= 2:
            break
    flush()

    if not examples:
        fallback_japanese, fallback_vi = make_fallback_example(lesson_title, pattern)
        examples.append(
            {
                "japanese_text": fallback_japanese,
                "reading": None,
                "meaning_vi": fallback_vi,
            }
        )
    return examples[:2]


def looks_like_heading_text(value: str) -> bool:
    return is_upper_toc_title(value) and len(value) < 80


def looks_like_example_sentence(value: str) -> bool:
    return bool(re.search(r"[。？！?]$", value)) or value.startswith(("Q：", "A："))


def is_clean_japanese_example(value: str) -> bool:
    if not has_japanese(value):
        return False
    if looks_like_heading_text(value):
        return False
    if re.search(r"\b(Câu|Cách dùng|Ý nghĩa|Chú ý|VD|Thể|Danh từ|Động từ)\b", value, flags=re.IGNORECASE):
        return False
    if re.search(r"\b[NVASQ]\d?\b|V\d|A\s*(い|な)|N\s*(を|に|で)?\s*V", value):
        return False
    if any(token in value for token in ["→", "＋", "+", "／", "[", "]", "。。。"]):
        return False
    japanese_chars = len(re.findall(r"[\u3040-\u30ff\u3400-\u9fff]", value))
    latin_chars = len(re.findall(r"[A-Za-zÀ-ỹ]", value))
    if japanese_chars < 4:
        return False
    if latin_chars > japanese_chars:
        return False
    if not (
        re.search(r"[。？！?]$", value)
        or any(
            ending in value
            for ending in [
                "です",
                "ます",
                "ません",
                "ました",
                "ください",
                "しょう",
                "んです",
                "できます",
                "られます",
                "れます",
            ]
        )
    ):
        return False
    return True


def make_fallback_example(title: str, pattern: str) -> tuple[str, str]:
    source = f"{title} {pattern}".lower()
    if "tính từ bổ nghĩa" in source:
        return "これは新しい本です。", "Đây là quyển sách mới."
    if "tính từ" in source and "khẳng định" in source:
        return "桜はきれいです。", "Hoa anh đào đẹp."
    if "tính từ" in source and "phủ định" in source:
        return "今日は暑くないです。", "Hôm nay không nóng."
    if "như thế nào" in source:
        return "日本の生活はどうですか。", "Cuộc sống ở Nhật thế nào?"
    if "cái nào" in source or "nào?" in source:
        return "あなたのかばんはどれですか。", "Cái cặp của bạn là cái nào?"
    if "và, hơn nữa" in source or "そして" in pattern:
        return "ナムさんはハンサムです。そして、親切です。", "Nam đẹp trai, hơn nữa còn tốt bụng."
    if "nhưng" in source or "けど" in source or "が" == pattern.strip():
        return "この料理はおいしいですが、高いです。", "Món này ngon nhưng đắt."
    if "liệt kê" in source or "たり" in pattern:
        return "日曜日は映画を見たり、本を読んだりします。", "Chủ nhật tôi xem phim, đọc sách..."
    if "trở nên" in source or "trở thành" in source or "なります" in pattern:
        return "日本語が上手になりました。", "Tiếng Nhật của tôi đã trở nên giỏi hơn."
    if "đã từng" in source or "たこと" in pattern:
        return "日本へ行ったことがあります。", "Tôi đã từng đi Nhật."
    if "trước" in source and "まえ" in pattern:
        return "寝る前に歯を磨きます。", "Trước khi ngủ tôi đánh răng."
    if "sau khi" in source or "てから" in pattern or "たら" in pattern:
        return "ご飯を食べてから、勉強します。", "Sau khi ăn cơm, tôi học."
    if "nghĩ" in source or "おもいます" in pattern:
        return "明日は雨が降ると思います。", "Tôi nghĩ ngày mai trời sẽ mưa."
    if "trích dẫn" in source or "といいます" in pattern:
        return "先生は「宿題を出してください」と言いました。", "Thầy cô đã nói: hãy nộp bài tập."
    if "phủ định" in source or "じゃありません" in pattern:
        return "私は医者じゃありません。", "Tôi không phải là bác sĩ."
    if "nghi vấn" in source or "ですか" in pattern:
        return "ミンさんは学生ですか。", "Anh Minh là học sinh phải không?"
    if "trợ từ の" in source or "の" == pattern.strip():
        return "私はハノイ大学の学生です。", "Tôi là sinh viên của Đại học Hà Nội."
    if "trợ từ も" in source or "も" in pattern:
        return "私もベトナム人です。", "Tôi cũng là người Việt Nam."
    if "これ" in pattern or "cái này" in source:
        return "これは時計です。", "Đây là đồng hồ."
    if "どこ" in pattern or "ở đâu" in source:
        return "トイレはどこですか。", "Nhà vệ sinh ở đâu?"
    if "いくら" in pattern or "giá" in source:
        return "このかばんはいくらですか。", "Cái cặp này giá bao nhiêu?"
    if "ください" in pattern or "hãy" in source:
        return "名前を書いてください。", "Hãy viết tên."
    if "ないで" in pattern or "đừng" in source:
        return "ここで写真を撮らないでください。", "Xin đừng chụp ảnh ở đây."
    if "てもいい" in pattern or "cũng được" in source:
        return "ここに座ってもいいです。", "Ngồi ở đây cũng được."
    if "てはいけません" in pattern or "không được" in source:
        return "ここでたばこを吸ってはいけません。", "Không được hút thuốc ở đây."
    if "なければ" in pattern or "bắt buộc" in source or "phải làm" in source:
        return "毎日薬を飲まなければなりません。", "Mỗi ngày tôi phải uống thuốc."
    if "たい" in pattern or "muốn" in source:
        return "日本へ行きたいです。", "Tôi muốn đi Nhật."
    if "あります" in pattern or "có" in source:
        return "机の上に本があります。", "Trên bàn có sách."
    if "います" in pattern:
        return "教室に学生がいます。", "Trong lớp có học sinh."
    if "から" in pattern or "vì" in source:
        return "忙しいですから、朝ご飯を食べません。", "Vì bận nên tôi không ăn sáng."
    if "とき" in pattern or "khi" in source:
        return "暇なとき、本を読みます。", "Khi rảnh tôi đọc sách."
    if "たら" in pattern or "nếu" in source:
        return "雨が降ったら、行きません。", "Nếu trời mưa thì tôi không đi."
    if "です" in pattern or "khẳng định" in source:
        return "私は学生です。", "Tôi là học sinh."
    return "日本語を勉強します。", f"Ví dụ minh họa cho mẫu: {title}."


def sql_value(value):
    if value is None:
        return "NULL"
    if isinstance(value, bool):
        return "TRUE" if value else "FALSE"
    if isinstance(value, int):
        return str(value)
    escaped = str(value).replace("\\", "\\\\").replace("'", "''")
    return f"'{escaped}'"


def insert_rows(table: str, columns: list[str], rows: list[dict], update_columns: list[str]) -> str:
    values = ",\n".join(
        "(" + ", ".join(sql_value(row.get(column)) for column in columns) + ")" for row in rows
    )
    updates = ",\n    ".join(f"{column} = VALUES({column})" for column in update_columns)
    return (
        f"INSERT INTO {table} ({', '.join(columns)}) VALUES\n"
        f"{values}\n"
        f"ON DUPLICATE KEY UPDATE\n    {updates};"
    )


def main() -> None:
    folder = find_n4_grammar_folder()
    files = sorted(folder.glob("*.pdf"), key=chapter_number_from_name)

    grammar_chapters: list[dict] = []
    grammar_lessons: list[dict] = []
    grammar_examples: list[dict] = []
    source_files: list[dict] = []

    lesson_id = GRAMMAR_LESSON_START_ID
    example_id = GRAMMAR_EXAMPLE_START_ID

    for file_path in files:
        chapter_number = chapter_number_from_name(file_path)
        chapter_id = GRAMMAR_CHAPTER_START_ID + chapter_number - 1
        lines = extract_lines(file_path)
        headings = pick_headings(lines)

        grammar_chapters.append(
            {
                "id": chapter_id,
                "jlpt_level_id": JLPT_LEVEL_ID,
                "chapter_number": chapter_number,
        "name": f"Bài {chapter_number}",
        "description": f"Ngữ pháp N4 - Bài {chapter_number}",
                "display_order": chapter_number,
                "is_published": True,
                "version": 1,
            }
        )
        source_files.append(
            {
                "chapter_number": chapter_number,
                "file_name": file_path.name,
                "parsed_lessons": len(headings),
            }
        )

        for order, heading in enumerate(headings, start=1):
            next_heading = headings[order]["index"] if order < len(headings) else None
            body = lesson_body(lines, heading, next_heading)
            title = heading["title"]
            pattern = extract_pattern(title, body)
            explanation = extract_explanation(title, body)
            formation = extract_formation(pattern, body)

            grammar_lessons.append(
                {
                    "id": lesson_id,
                    "grammar_chapter_id": chapter_id,
                    "title": title,
                    "pattern": pattern,
                    "meaning_vi": title,
                    "explanation": explanation,
                    "formation": formation,
                    "jlpt_level_id": JLPT_LEVEL_ID,
                    "display_order": order,
                    "is_published": True,
                    "version": 1,
                }
            )

            for example_order, example in enumerate(extract_examples(body, title, pattern), start=1):
                grammar_examples.append(
                    {
                        "id": example_id,
                        "grammar_lesson_id": lesson_id,
                        "japanese_text": example["japanese_text"],
                        "reading": example["reading"],
                        "meaning_vi": example["meaning_vi"],
                        "display_order": example_order,
                    }
                )
                example_id += 1

            lesson_id += 1

    output = {
        "metadata": {
            "name": "JLPT N4 grammar import data by chapter",
            "source_folder": str(folder),
            "jlpt_level_id_assumption": JLPT_LEVEL_ID,
            "generated_from": "PDF text layer in plan/ngữ pháp n4",
            "import_order": ["grammar_chapters", "grammar_lessons", "grammar_examples"],
            "notes": [
                "One grammar_chapter is created for each PDF lesson Bài 26-50.",
                "Lessons are parsed from numbered headings in each PDF.",
                "Example rows are extracted from visible VD sections when possible; otherwise a short fallback example is generated.",
            ],
        },
        "source_files": source_files,
        "grammar_chapters": grammar_chapters,
        "grammar_lessons": grammar_lessons,
        "grammar_examples": grammar_examples,
    }

    OUTPUT_JSON_PATH.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    chapter_columns = [
        "id",
        "jlpt_level_id",
        "chapter_number",
        "name",
        "description",
        "display_order",
        "is_published",
        "version",
    ]
    lesson_columns = [
        "id",
        "grammar_chapter_id",
        "title",
        "pattern",
        "meaning_vi",
        "explanation",
        "formation",
        "jlpt_level_id",
        "display_order",
        "is_published",
        "version",
    ]
    example_columns = [
        "id",
        "grammar_lesson_id",
        "japanese_text",
        "reading",
        "meaning_vi",
        "display_order",
    ]

    sql_parts = [
        "SET NAMES utf8mb4;",
        (
            "DELETE ge FROM grammar_examples ge "
            "JOIN grammar_lessons gl ON gl.id = ge.grammar_lesson_id "
            f"WHERE gl.jlpt_level_id = {JLPT_LEVEL_ID};"
        ),
        f"DELETE FROM grammar_lessons WHERE jlpt_level_id = {JLPT_LEVEL_ID};",
        f"DELETE FROM grammar_chapters WHERE jlpt_level_id = {JLPT_LEVEL_ID};",
        insert_rows(
            "grammar_chapters",
            chapter_columns,
            grammar_chapters,
            ["jlpt_level_id", "chapter_number", "name", "description", "display_order", "is_published", "version"],
        ),
        insert_rows(
            "grammar_lessons",
            lesson_columns,
            grammar_lessons,
            [
                "grammar_chapter_id",
                "title",
                "pattern",
                "meaning_vi",
                "explanation",
                "formation",
                "jlpt_level_id",
                "display_order",
                "is_published",
                "version",
            ],
        ),
        insert_rows(
            "grammar_examples",
            example_columns,
            grammar_examples,
            ["grammar_lesson_id", "japanese_text", "reading", "meaning_vi", "display_order"],
        ),
    ]
    OUTPUT_SQL_PATH.write_text("\n\n".join(sql_parts) + "\n", encoding="utf-8")

    print(f"created {OUTPUT_JSON_PATH}")
    print(f"created {OUTPUT_SQL_PATH}")
    print(
        f"{len(grammar_chapters)} grammar chapters, "
        f"{len(grammar_lessons)} grammar lessons, "
        f"{len(grammar_examples)} grammar examples"
    )
    for item in source_files:
        print(f"Bài {item['chapter_number']:02d}: {item['parsed_lessons']} lessons")


if __name__ == "__main__":
    main()
