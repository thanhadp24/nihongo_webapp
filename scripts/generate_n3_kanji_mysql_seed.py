import json
from pathlib import Path


INPUT = Path("database/import/jlpt_n3_kanji_by_topic_db_import.json")
OUTPUT = Path("database/seed/011_jlpt_n3_kanji.sql")

def sql_value(value):
    if value is None:
        return "NULL"
    if isinstance(value, bool):
        return "TRUE" if value else "FALSE"
    if isinstance(value, int):
        return str(value)
    text = str(value).replace("\\", "\\\\").replace("'", "''")
    return f"'{text}'"


def row(values):
    return "(" + ", ".join(sql_value(value) for value in values) + ")"


def build_sql(data: dict) -> str:
    topic_id_map = {topic["id"]: topic["id"] for topic in data["kanji_topics"]}
    char_id_map = {char["id"]: char["id"] for char in data["kanji_characters"]}
    word_id_map = {word["id"]: word["id"] for word in data["kanji_words"]}

    lines = [
        "SET NAMES utf8mb4;",
        "START TRANSACTION;",
        "",
        "-- Re-import JLPT N3 Kanji only. Child rows are removed by ON DELETE CASCADE.",
        "-- IDs are kept natural for a fresh kanji dataset: topics 1..36, characters 1..n, words 1..n.",
        "DELETE FROM kanji_topics WHERE jlpt_level_id = 3;",
        "",
    ]

    topic_columns = [
        "id",
        "jlpt_level_id",
        "name",
        "name_reading",
        "name_vi",
        "description",
        "source_book",
        "source_week",
        "source_week_title",
        "source_week_title_vi",
        "source_day",
        "source_page_start",
        "source_url",
        "display_order",
        "is_published",
        "version",
    ]
    topic_rows = [
        row(
            [
                topic_id_map[topic["id"]],
                topic["jlpt_level_id"],
                topic["name"],
                topic.get("name_reading"),
                topic.get("name_vi"),
                topic.get("description"),
                topic.get("source_book"),
                topic.get("source_week"),
                topic.get("source_week_title"),
                topic.get("source_week_title_vi"),
                topic.get("source_day"),
                topic.get("source_page_start"),
                topic.get("source_url"),
                topic.get("display_order", 0),
                topic.get("is_published", True),
                topic.get("version", 1),
            ]
        )
        for topic in data["kanji_topics"]
    ]
    lines.append(f"INSERT INTO kanji_topics ({', '.join(topic_columns)}) VALUES")
    lines.append(",\n".join(topic_rows) + ";")
    lines.append("")

    character_columns = [
        "id",
        "kanji_topic_id",
        "character_value",
        "han_viet",
        "onyomi",
        "kunyomi",
        "meaning_vi",
        "stroke_count",
        "mnemonic_vi",
        "display_order",
        "is_published",
        "version",
    ]
    character_rows = [
        row(
            [
                char_id_map[char["id"]],
                topic_id_map[char["kanji_topic_id"]],
                char["character_value"],
                char.get("han_viet"),
                char.get("onyomi"),
                char.get("kunyomi"),
                char.get("meaning_vi"),
                char.get("stroke_count"),
                char.get("mnemonic_vi"),
                char.get("display_order", 0),
                char.get("is_published", True),
                char.get("version", 1),
            ]
        )
        for char in data["kanji_characters"]
    ]
    lines.append(f"INSERT INTO kanji_characters ({', '.join(character_columns)}) VALUES")
    lines.append(",\n".join(character_rows) + ";")
    lines.append("")

    word_columns = [
        "id",
        "kanji_character_id",
        "word",
        "reading",
        "meaning_vi",
        "example_sentence",
        "example_reading",
        "example_meaning_vi",
        "display_order",
        "is_published",
        "version",
    ]
    word_rows = [
        row(
            [
                word_id_map[word["id"]],
                char_id_map[word["kanji_character_id"]],
                word["word"],
                word.get("reading"),
                word.get("meaning_vi"),
                word.get("example_sentence"),
                word.get("example_reading"),
                word.get("example_meaning_vi"),
                word.get("display_order", 0),
                word.get("is_published", True),
                word.get("version", 1),
            ]
        )
        for word in data["kanji_words"]
    ]
    lines.append(f"INSERT INTO kanji_words ({', '.join(word_columns)}) VALUES")
    lines.append(",\n".join(word_rows) + ";")
    lines.append("")
    lines.append(f"ALTER TABLE kanji_topics AUTO_INCREMENT = {max(topic_id_map.values()) + 1};")
    lines.append(f"ALTER TABLE kanji_characters AUTO_INCREMENT = {max(char_id_map.values()) + 1};")
    lines.append(f"ALTER TABLE kanji_words AUTO_INCREMENT = {max(word_id_map.values()) + 1};")
    lines.append("")
    lines.append("COMMIT;")
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    data = json.loads(INPUT.read_text(encoding="utf-8"))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(build_sql(data), encoding="utf-8")
    print(f"Wrote {OUTPUT}")
    print(f"topics={len(data['kanji_topics'])}")
    print(f"kanji_characters={len(data['kanji_characters'])}")
    print(f"kanji_words={len(data['kanji_words'])}")
