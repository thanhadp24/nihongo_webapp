import json
import math
import re
from pathlib import Path

import fitz


JLPT_LEVEL_ID = 3
GRAMMAR_CHAPTER_START_ID = 51
GRAMMAR_LESSON_START_ID = 233
GRAMMAR_EXAMPLE_START_ID = 297

SOURCE_PDF_GLOB = "*Ebook N3.pdf"
OUTPUT_JSON_PATH = Path("database/import/jlpt_n3_grammar_by_chapter_db_import.json")
OUTPUT_SQL_PATH = Path("database/seed/009_jlpt_n3_grammar.sql")


def clean_line(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def source_pdf() -> Path:
    matches = list(Path("plan").glob(SOURCE_PDF_GLOB))
    if not matches:
        raise FileNotFoundError(f"Could not find {SOURCE_PDF_GLOB} in plan/")
    return matches[0]


def has_japanese(value: str) -> bool:
    return bool(re.search(r"[\u3040-\u30ff\u3400-\u9fff]", value))


def strip_footer(lines: list[str]) -> list[str]:
    result: list[str] = []
    for line in lines:
        if "Nhật ngữ VTI Mirai" in line or "Website:" in line:
            break
        result.append(line)
    while result and re.fullmatch(r"\d{1,3}", result[-1]):
        result.pop()
    return result


def extract_blocks(path: Path) -> list[dict]:
    blocks: list[dict] = []
    doc = fitz.open(path)

    for page_number, page in enumerate(doc, start=1):
        lines = [clean_line(line) for line in page.get_text().splitlines()]
        lines = [line for line in lines if line]
        starts: list[tuple[int, int]] = []

        for index, line in enumerate(lines):
            if not re.fullmatch(r"\d{1,3}", line):
                continue
            number = int(line)
            previous = " ".join(lines[max(0, index - 3) : index])
            if "Website:" in previous or "Nhật ngữ VTI Mirai" in previous:
                continue
            if 1 <= number <= 90:
                starts.append((index, number))

        for start_index, (line_index, number) in enumerate(starts):
            end_index = starts[start_index + 1][0] if start_index + 1 < len(starts) else len(lines)
            body = strip_footer(lines[line_index + 1 : end_index])
            if len(body) < 2:
                continue
            blocks.append({"number": number, "page": page_number, "body": body})

    unique: dict[int, dict] = {}
    for block in blocks:
        unique[block["number"]] = block

    return [unique[number] for number in sorted(unique)]


def looks_like_title_line(line: str) -> bool:
    if not line or line.startswith(("-", "*")):
        return False
    if "Website:" in line:
        return False
    if any(word in line for word in ["Tôn kính ngữ", "Khiêm nhường ngữ", "尊敬語", "謙譲語"]):
        return True
    if has_japanese(line) and any(token in line for token in ["～", ":", "：", "＋", "+"]):
        return True
    if "～" in line and has_japanese(line):
        return True
    return False


def title_line(body: list[str]) -> str:
    for line in body:
        if any(word in line for word in ["Tôn kính ngữ", "Khiêm nhường ngữ", "尊敬語", "謙譲語"]):
            return line
    for line in reversed(body):
        if looks_like_title_line(line):
            return line
    for line in body:
        if not line.startswith(("-", "*")) and (has_japanese(line) or looks_vietnamese(line)):
            return line
    return "Mẫu ngữ pháp N3"


def split_pattern_and_meaning(line: str) -> tuple[str, str]:
    normalized = line.strip()
    for separator in ["：", ":"]:
        if separator in normalized:
            left, right = normalized.rsplit(separator, 1)
            if left.strip() and right.strip():
                return left.strip(), right.strip()
    return normalized, normalized


def looks_vietnamese(line: str) -> bool:
    if has_japanese(line):
        return False
    return bool(re.search(r"[A-Za-zÀ-ỹ]", line))


def extract_explanation(body: list[str]) -> str:
    explanation_parts: list[str] = []
    capture_following_bullet = False

    for line in body:
        if looks_like_title_line(line):
            break
        if line.startswith("*"):
            text = line.lstrip("*").strip()
            if text:
                explanation_parts.append(text)
            capture_following_bullet = True
            continue
        if line.startswith("-"):
            capture_following_bullet = False
            continue
        if capture_following_bullet and looks_vietnamese(line):
            explanation_parts.append(line)
        if len(" ".join(explanation_parts)) > 700:
            break

    if not explanation_parts:
        for line in body[:5]:
            if looks_vietnamese(line):
                explanation_parts.append(line)

    text = " ".join(explanation_parts)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:900] if text else "Mẫu ngữ pháp N3."


def clean_meaning(value: str) -> str:
    value = re.sub(r"\s+", " ", value).strip()
    value = re.split(r"\s*[❖*]\s*|\s+[-–]\s+Website", value, maxsplit=1)[0].strip()
    if len(value) > 240:
        clipped = value[:240]
        last_stop = max(clipped.rfind("."), clipped.rfind("?"), clipped.rfind("!"))
        if last_stop > 40:
            clipped = clipped[: last_stop + 1]
        value = clipped
    return value


def is_japanese_sentence(line: str) -> bool:
    if not has_japanese(line):
        return False
    if any(token in line for token in ["→", "＋", "[", "]", "Website:"]):
        return False
    japanese_chars = len(re.findall(r"[\u3040-\u30ff\u3400-\u9fff]", line))
    latin_chars = len(re.findall(r"[A-Za-zÀ-ỹ]", line))
    if japanese_chars < 5:
        return False
    if latin_chars > japanese_chars:
        return False
    return True


def extract_parenthetical_vi(line: str) -> tuple[str, str | None]:
    match = re.search(r"(.+?)\(([^()]*[A-Za-zÀ-ỹ][^()]*)\)\s*$", line)
    if not match:
        return line, None
    return match.group(1).strip(), clean_meaning(match.group(2))


def extract_examples(body: list[str], pattern: str, title: str) -> list[dict]:
    examples: list[dict] = []
    index = 0
    while index < len(body):
        line = body[index]
        if not line.startswith("-"):
            index += 1
            continue

        japanese = line.lstrip("-").strip()
        continuation_index = index + 1
        while continuation_index < min(index + 5, len(body)):
            continuation = body[continuation_index]
            if continuation.startswith("-") or looks_like_title_line(continuation):
                break
            has_unclosed_parenthesis = (
                japanese.count("(") > japanese.count(")")
                or japanese.count("（") > japanese.count("）")
            )
            if has_japanese(continuation) or has_unclosed_parenthesis:
                separator = "" if has_japanese(continuation) else " "
                japanese = f"{japanese}{separator}{continuation}"
                continuation_index += 1
                continue
            break
        japanese, inline_vi = extract_parenthetical_vi(japanese)
        if not is_japanese_sentence(japanese):
            index += 1
            continue

        meaning_parts: list[str] = []
        if inline_vi:
            meaning_parts.append(inline_vi)

        lookahead = continuation_index
        while lookahead < min(index + 5, len(body)):
            next_line = body[lookahead]
            if next_line.startswith("-") or looks_like_title_line(next_line):
                break
            if looks_vietnamese(next_line):
                meaning_parts.append(next_line)
            elif has_japanese(next_line):
                break
            lookahead += 1

        meaning = clean_meaning(" ".join(meaning_parts))
        if meaning:
            examples.append(
                {
                    "japanese_text": japanese[:500],
                    "reading": None,
                    "meaning_vi": meaning,
                }
            )
        index += 1
        if len(examples) >= 2:
            break

    if not examples:
        japanese, meaning = fallback_example(pattern, title)
        examples.append({"japanese_text": japanese, "reading": None, "meaning_vi": meaning})

    return examples[:2]


def fallback_example(pattern: str, title: str) -> tuple[str, str]:
    source = f"{pattern} {title}"
    if "うちに" in source:
        return "日本にいるうちに富士山に登りたいです。", "Trong lúc còn ở Nhật, tôi muốn leo núi Phú Sĩ."
    if "間" in source:
        return "母が寝ている間、子どもはテレビを見ていました。", "Trong khi mẹ đang ngủ, bọn trẻ xem tivi."
    if "ところ" in source:
        return "今、出かけるところです。", "Bây giờ tôi sắp ra ngoài."
    if "たびに" in source:
        return "この写真を見るたびに、家族を思い出します。", "Mỗi lần xem bức ảnh này, tôi nhớ gia đình."
    if "ほど" in source:
        return "練習すればするほど上手になります。", "Càng luyện tập thì càng giỏi."
    if "ついで" in source:
        return "買い物のついでに手紙を出しました。", "Nhân tiện đi mua sắm, tôi đã gửi thư."
    if "によって" in source:
        return "国によって習慣が違います。", "Tập quán khác nhau tùy từng nước."
    if "そう" in source or "らしい" in source:
        return "明日は雨が降るそうです。", "Nghe nói ngày mai trời sẽ mưa."
    if "はず" in source:
        return "田中さんはもう着いたはずです。", "Chắc là anh Tanaka đã đến rồi."
    if "ことに" in source:
        return "毎朝牛乳を飲むことにしています。", "Tôi quyết định duy trì uống sữa mỗi sáng."
    if "尊敬語" in source:
        return "社長はもう帰られました。", "Giám đốc đã về rồi."
    if "謙譲語" in source:
        return "山田と申します。", "Tôi tên là Yamada."
    return "日本語を勉強しています。", f"Ví dụ minh họa cho mẫu: {title}."


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
    path = source_pdf()
    blocks = extract_blocks(path)
    blocks = [block for block in blocks if 1 <= block["number"] <= 62]
    expected = set(range(1, 63))
    parsed = {block["number"] for block in blocks}
    missing = sorted(expected - parsed)
    if missing:
        raise RuntimeError(f"Missing N3 grammar numbers: {missing}")

    grammar_chapters: list[dict] = []
    grammar_lessons: list[dict] = []
    grammar_examples: list[dict] = []

    chapter_count = math.ceil(len(blocks) / 5)
    for chapter_order in range(1, chapter_count + 1):
        start_number = (chapter_order - 1) * 5 + 1
        end_number = min(chapter_order * 5, len(blocks))
        grammar_chapters.append(
            {
                "id": GRAMMAR_CHAPTER_START_ID + chapter_order - 1,
                "jlpt_level_id": JLPT_LEVEL_ID,
                "chapter_number": chapter_order,
                "name": f"Bài {chapter_order} (Mẫu {start_number}-{end_number})",
                "description": f"Ngữ pháp N3 - Mẫu {start_number}-{end_number}",
                "display_order": chapter_order,
                "is_published": True,
                "version": 1,
            }
        )

    example_id = GRAMMAR_EXAMPLE_START_ID
    for block in blocks:
        number = block["number"]
        chapter_order = math.ceil(number / 5)
        grammar_chapter_id = GRAMMAR_CHAPTER_START_ID + chapter_order - 1
        lesson_id = GRAMMAR_LESSON_START_ID + number - 1
        order_in_chapter = ((number - 1) % 5) + 1
        raw_title = title_line(block["body"])
        pattern, meaning = split_pattern_and_meaning(raw_title)
        if meaning == pattern:
            try:
                title_index = block["body"].index(raw_title)
            except ValueError:
                title_index = -1
            if title_index >= 0 and title_index + 1 < len(block["body"]):
                next_line = block["body"][title_index + 1]
                if looks_vietnamese(next_line) and next_line != "Ví dụ" and not next_line.startswith(("-", "*")):
                    meaning = next_line
        title = f"Mẫu {number} - {pattern}"
        explanation = extract_explanation(block["body"])
        examples = extract_examples(block["body"], pattern, title)

        grammar_lessons.append(
            {
                "id": lesson_id,
                "grammar_chapter_id": grammar_chapter_id,
                "title": title[:255],
                "pattern": pattern[:255],
                "meaning_vi": meaning[:500],
                "explanation": explanation,
                "formation": pattern,
                "jlpt_level_id": JLPT_LEVEL_ID,
                "display_order": order_in_chapter,
                "is_published": True,
                "version": 1,
            }
        )

        for display_order, example in enumerate(examples, start=1):
            grammar_examples.append(
                {
                    "id": example_id,
                    "grammar_lesson_id": lesson_id,
                    "japanese_text": example["japanese_text"],
                    "reading": example["reading"],
                    "meaning_vi": example["meaning_vi"],
                    "display_order": display_order,
                }
            )
            example_id += 1

    output = {
        "metadata": {
            "name": "JLPT N3 grammar import data by grouped chapters",
            "source_file": str(path),
            "jlpt_level_id_assumption": JLPT_LEVEL_ID,
            "generated_from": "PDF text layer",
            "import_order": ["grammar_chapters", "grammar_lessons", "grammar_examples"],
            "notes": [
                "The source ebook is a numbered list, so grammar_chapters are generated by grouping every 5 grammar points.",
                "Lesson titles keep the original grammar point number from the PDF.",
                "Examples are extracted from visible Japanese example rows when possible; otherwise a short fallback example is generated.",
            ],
        },
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
    for chapter in grammar_chapters:
        count = sum(1 for lesson in grammar_lessons if lesson["grammar_chapter_id"] == chapter["id"])
        print(f"{chapter['name']}: {count} lessons")


if __name__ == "__main__":
    main()
