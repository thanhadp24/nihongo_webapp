import json
import re
from pathlib import Path

import fitz

try:
    import pykakasi
except ImportError:  # pragma: no cover - optional local generation helper
    pykakasi = None


JLPT_LEVEL_ID = 5
GRAMMAR_CHAPTER_START_ID = 90
GRAMMAR_LESSON_START_ID = 452
GRAMMAR_EXAMPLE_START_ID = 575

SOURCE_PDF_GLOB = "*SHINKANZEN N1*.pdf"
OUTPUT_JSON_PATH = Path("database/import/jlpt_n1_grammar_by_chapter_db_import.json")
OUTPUT_SQL_PATH = Path("database/seed/011_jlpt_n1_grammar.sql")

WAVE_CHARS = "\u301c\uff5e~"
HEADER_LINES = {
    "TỔNG HỢP NGỮ PHÁP SHINKANZEN N1",
    "Cách chia thể",
    "Cấu trúc NP",
    "Nghĩa ( tên gọi)",
    "Phạm vi sử dụng + chú ý",
    "VD minh họa ( tiếng việt)",
}


def source_pdf() -> Path:
    matches = list(Path("plan").glob(SOURCE_PDF_GLOB))
    if not matches:
        raise FileNotFoundError(f"Could not find {SOURCE_PDF_GLOB} in plan/")
    return matches[0]


def clean_line(value: str) -> str:
    value = value.replace("\uff5e", "～").replace("\u301c", "～").replace("~", "～")
    return re.sub(r"\s+", " ", value).strip()


def has_japanese(value: str) -> bool:
    normalized = value.replace("・", "")
    return bool(re.search(r"[\u3040-\u30fa\u30fc-\u30ff\u3400-\u9fff]", normalized))


def has_wave(value: str) -> bool:
    return any(char in value for char in WAVE_CHARS)


def is_chapter_line(value: str) -> bool:
    return bool(re.fullmatch(r"Bài số\s+\d+", value))


def is_header_line(value: str) -> bool:
    return value in HEADER_LINES


def is_vietnamese_text(value: str) -> bool:
    if has_japanese(value):
        return False
    return bool(re.search(r"[A-Za-zÀ-ỹ]", value))


def extract_blocks(path: Path) -> list[dict]:
    doc = fitz.open(path)
    blocks: list[dict] = []
    current_lines: list[str] = []
    current_chapter: int | None = None
    in_watermark = False

    def flush() -> None:
        nonlocal current_lines
        if current_lines and any(has_wave(line) for line in current_lines):
            blocks.append({"chapter_number": current_chapter, "lines": current_lines[:]})
        current_lines = []

    for page in doc:
        lines = [clean_line(line) for line in page.get_text().splitlines()]
        lines = [line for line in lines if line]

        for line in lines:
            if line == "MINATODORIMU":
                if not in_watermark:
                    flush()
                in_watermark = True
                continue

            in_watermark = False

            if is_chapter_line(line):
                flush()
                current_chapter = int(re.search(r"\d+", line).group())
                continue

            if is_header_line(line):
                continue

            current_lines.append(line)

    flush()

    for index, block in enumerate(blocks, start=1):
        if block["chapter_number"] is None:
            raise RuntimeError(f"Could not assign chapter for N1 grammar block {index}: {block['lines'][:6]}")

    return blocks


def pattern_start_index(lines: list[str]) -> int:
    for index, line in enumerate(lines):
        if has_wave(line):
            return index
    raise ValueError(f"Could not find pattern line in block: {lines[:10]}")


def pattern_parts(lines: list[str]) -> tuple[list[str], list[str], int]:
    start = pattern_start_index(lines)
    parts: list[str] = []
    inline_meaning_parts: list[str] = []
    index = start

    while index < len(lines):
        line = lines[index]
        if line.startswith("•") or line.startswith("VD"):
            break
        if parts and is_vietnamese_text(line):
            break

        line, inline_meaning = split_inline_pattern_meaning(line)
        if has_wave(line):
            parts.append(line)
        elif parts:
            parts[-1] += line
        if inline_meaning:
            inline_meaning_parts.append(inline_meaning)
        index += 1

    return parts, inline_meaning_parts, index


def split_inline_pattern_meaning(line: str) -> tuple[str, str | None]:
    if "・" not in line:
        return line, None
    left, right = line.split("・", 1)
    if has_wave(left) and is_vietnamese_text(right):
        return left.strip(), right.strip()
    return line, None


def normalize_pattern(parts: list[str]) -> str:
    cleaned: list[str] = []
    for part in parts:
        part = clean_line(part)
        part = re.sub(r"～\s+", "～", part)
        part = re.sub(r"\s+", " ", part)
        if part:
            cleaned.append(part)
    return " / ".join(cleaned)


def split_block(block: dict) -> dict:
    lines = block["lines"]
    parts, inline_meaning_parts, after_pattern = pattern_parts(lines)
    pattern = normalize_pattern(parts)

    bullet_index = next(
        (index for index, line in enumerate(lines[after_pattern:], start=after_pattern) if line.startswith("•")),
        len(lines),
    )
    vd_index = next(
        (index for index, line in enumerate(lines) if line.startswith("VD")),
        len(lines),
    )

    meaning_lines = inline_meaning_parts + lines[after_pattern : min(bullet_index, vd_index)]
    meaning_vi = clean_meaning(" ".join(meaning_lines))

    explanation_lines = lines[bullet_index:vd_index] if bullet_index < vd_index else []
    explanation = clean_explanation(" ".join(explanation_lines))

    japanese_text, example_meaning_vi = extract_example(lines[vd_index:] if vd_index < len(lines) else [])

    return {
        "chapter_number": block["chapter_number"],
        "pattern": pattern,
        "meaning_vi": meaning_vi or pattern,
        "explanation": explanation or f"Dùng để diễn đạt ý '{meaning_vi or pattern}'.",
        "japanese_text": japanese_text,
        "reading": to_hiragana(japanese_text) if japanese_text else None,
        "example_meaning_vi": example_meaning_vi,
    }


def clean_meaning(value: str) -> str:
    value = value.replace("・", " ")
    value = re.sub(r"\s+", " ", value).strip(" .。")
    return value[:500]


def clean_explanation(value: str) -> str:
    value = value.replace("•", " ")
    value = re.sub(r"\s+", " ", value).strip()
    if len(value) > 900:
        clipped = value[:900]
        last_stop = max(clipped.rfind("."), clipped.rfind("。"), clipped.rfind("!"), clipped.rfind("?"))
        value = clipped[: last_stop + 1] if last_stop > 80 else clipped
    return value


def extract_example(lines: list[str]) -> tuple[str | None, str | None]:
    if not lines:
        return None, None

    japanese_parts: list[str] = []
    meaning_parts: list[str] = []
    collecting_japanese = False
    collecting_meaning = False

    for index, line in enumerate(lines):
        if index == 0:
            line = re.sub(r"^VD\s*[：:]\s*", "", line).strip()
            if not line:
                continue

        if has_japanese(line):
            if not collecting_meaning:
                collecting_japanese = True
                japanese_parts.append(line)
            continue

        if collecting_japanese and is_vietnamese_text(line):
            collecting_meaning = True
            meaning_parts.append(line)
            continue

        if collecting_meaning and is_vietnamese_text(line):
            meaning_parts.append(line)

    japanese_text = clean_line("".join(japanese_parts)) if japanese_parts else None
    meaning_vi = clean_meaning(" ".join(meaning_parts)) if meaning_parts else None
    return japanese_text, meaning_vi


def to_hiragana(value: str | None) -> str | None:
    if not value or pykakasi is None:
        return None
    kakasi = to_hiragana.kakasi
    return "".join(item["hira"] for item in kakasi.convert(value))


if pykakasi is not None:
    to_hiragana.kakasi = pykakasi.kakasi()


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


def build_data() -> dict:
    path = source_pdf()
    blocks = extract_blocks(path)
    lessons = [split_block(block) for block in blocks]

    chapter_numbers = sorted({lesson["chapter_number"] for lesson in lessons})
    grammar_chapters: list[dict] = []
    grammar_lessons: list[dict] = []
    grammar_examples: list[dict] = []

    lesson_id = GRAMMAR_LESSON_START_ID
    example_id = GRAMMAR_EXAMPLE_START_ID

    for display_order, chapter_number in enumerate(chapter_numbers, start=1):
        chapter_lessons = [lesson for lesson in lessons if lesson["chapter_number"] == chapter_number]
        chapter_id = GRAMMAR_CHAPTER_START_ID + chapter_number - 1
        first_lesson_id = lesson_id
        last_lesson_id = lesson_id + len(chapter_lessons) - 1
        grammar_chapters.append(
            {
                "id": chapter_id,
                "jlpt_level_id": JLPT_LEVEL_ID,
                "chapter_number": chapter_number,
                "name": f"Bài {chapter_number}",
                "description": (
                    f"Ngữ pháp N1 Shinkanzen - Bài {chapter_number} "
                    f"({len(chapter_lessons)} mẫu, lesson {first_lesson_id}-{last_lesson_id})"
                ),
                "display_order": display_order,
                "is_published": True,
                "version": 1,
            }
        )

        for order_in_chapter, lesson in enumerate(chapter_lessons, start=1):
            title = f"Bài {chapter_number}.{order_in_chapter} - {lesson['pattern']}"
            grammar_lessons.append(
                {
                    "id": lesson_id,
                    "grammar_chapter_id": chapter_id,
                    "title": title[:255],
                    "pattern": lesson["pattern"][:255],
                    "meaning_vi": lesson["meaning_vi"][:500],
                    "explanation": lesson["explanation"],
                    "formation": lesson["pattern"][:500],
                    "jlpt_level_id": JLPT_LEVEL_ID,
                    "display_order": order_in_chapter,
                    "is_published": True,
                    "version": 1,
                }
            )

            if lesson["japanese_text"] and lesson["example_meaning_vi"]:
                grammar_examples.append(
                    {
                        "id": example_id,
                        "grammar_lesson_id": lesson_id,
                        "japanese_text": lesson["japanese_text"],
                        "reading": lesson["reading"],
                        "meaning_vi": lesson["example_meaning_vi"],
                        "display_order": 1,
                    }
                )
                example_id += 1

            lesson_id += 1

    return {
        "metadata": {
            "name": "JLPT N1 grammar import data by Shinkanzen chapters",
            "source_file": str(path),
            "jlpt_level_id_assumption": JLPT_LEVEL_ID,
            "generated_from": "PDF text layer",
            "import_order": ["grammar_chapters", "grammar_lessons", "grammar_examples"],
            "notes": [
                "The source PDF is organized as Bài số 1-20; these are mapped directly to grammar_chapters.",
                "Grammar examples are extracted from the VD column.",
                "Example readings are generated with pykakasi when it is available locally.",
            ],
        },
        "grammar_chapters": grammar_chapters,
        "grammar_lessons": grammar_lessons,
        "grammar_examples": grammar_examples,
    }


def main() -> None:
    data = build_data()
    OUTPUT_JSON_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

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
            data["grammar_chapters"],
            ["jlpt_level_id", "chapter_number", "name", "description", "display_order", "is_published", "version"],
        ),
        insert_rows(
            "grammar_lessons",
            lesson_columns,
            data["grammar_lessons"],
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
            data["grammar_examples"],
            ["grammar_lesson_id", "japanese_text", "reading", "meaning_vi", "display_order"],
        ),
    ]
    OUTPUT_SQL_PATH.write_text("\n\n".join(sql_parts) + "\n", encoding="utf-8")

    print(f"created {OUTPUT_JSON_PATH}")
    print(f"created {OUTPUT_SQL_PATH}")
    print(
        f"{len(data['grammar_chapters'])} grammar chapters, "
        f"{len(data['grammar_lessons'])} grammar lessons, "
        f"{len(data['grammar_examples'])} grammar examples"
    )
    for chapter in data["grammar_chapters"]:
        count = sum(1 for lesson in data["grammar_lessons"] if lesson["grammar_chapter_id"] == chapter["id"])
        print(f"{chapter['name']}: {count} lessons")


if __name__ == "__main__":
    main()
