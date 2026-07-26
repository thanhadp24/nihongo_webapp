import argparse
import json
import os
from pathlib import Path
from urllib.parse import urlparse

import pymysql
from dotenv import load_dotenv


TOPIC_COLUMNS = [
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

CHARACTER_COLUMNS = [
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

WORD_COLUMNS = [
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


def load_database_config() -> dict:
    load_dotenv()
    database_url = os.environ.get("DATABASE_URL_LOCAL") or os.environ.get("DATABASE_URL")
    if database_url:
        parsed = urlparse(database_url)
        return {
            "host": parsed.hostname or os.environ.get("MYSQL_HOST", "127.0.0.1"),
            "port": parsed.port or int(os.environ.get("MYSQL_PORT", "3306")),
            "user": parsed.username or os.environ.get("MYSQL_USER", "nihongo"),
            "password": parsed.password or os.environ.get("MYSQL_PASSWORD", ""),
            "database": (parsed.path or "/nihongo_webapp").lstrip("/"),
        }

    return {
        "host": os.environ.get("MYSQL_HOST", "127.0.0.1"),
        "port": int(os.environ.get("MYSQL_PORT", "3306")),
        "user": os.environ.get("MYSQL_USER", "nihongo"),
        "password": os.environ.get("MYSQL_PASSWORD", ""),
        "database": os.environ.get("MYSQL_DATABASE", "nihongo_webapp"),
    }


def placeholders(columns: list[str]) -> str:
    return ", ".join(["%s"] * len(columns))


def insert_row(cursor, table: str, columns: list[str], row: dict) -> int:
    sql = (
        f"INSERT INTO {table} ({', '.join(columns)}) "
        f"VALUES ({placeholders(columns)})"
    )
    cursor.execute(sql, [row.get(column) for column in columns])
    return cursor.lastrowid


def ensure_no_note_fields(data: dict) -> None:
    for group in ("kanji_topics", "kanji_characters", "kanji_words"):
        for item in data[group]:
            if "note" in item:
                raise ValueError(f"Unexpected note field in {group}: {item}")


def import_kanji_json(path: Path, dry_run: bool = False) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    ensure_no_note_fields(data)

    jlpt_code = data.get("metadata", {}).get("jlpt_level_code")
    if not jlpt_code:
        raise ValueError("metadata.jlpt_level_code is required")

    config = load_database_config()
    connection = pymysql.connect(
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False,
        **config,
    )

    topic_id_map: dict[int, int] = {}
    character_id_map: dict[int, int] = {}

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id FROM jlpt_levels WHERE code = %s",
                (jlpt_code,),
            )
            level = cursor.fetchone()
            if not level:
                raise ValueError(f"JLPT level not found in database: {jlpt_code}")

            jlpt_level_id = level["id"]

            cursor.execute(
                """
                SELECT
                    COUNT(DISTINCT kt.id) AS topics,
                    COUNT(DISTINCT kc.id) AS characters,
                    COUNT(DISTINCT kw.id) AS words
                FROM kanji_topics kt
                LEFT JOIN kanji_characters kc ON kc.kanji_topic_id = kt.id
                LEFT JOIN kanji_words kw ON kw.kanji_character_id = kc.id
                WHERE kt.jlpt_level_id = %s
                """,
                (jlpt_level_id,),
            )
            before = cursor.fetchone()

            if dry_run:
                connection.rollback()
                return {
                    "jlpt_level_id": jlpt_level_id,
                    "before": before,
                    "imported_topics": len(data["kanji_topics"]),
                    "imported_characters": len(data["kanji_characters"]),
                    "imported_words": len(data["kanji_words"]),
                    "dry_run": True,
                }

            cursor.execute(
                "DELETE FROM kanji_topics WHERE jlpt_level_id = %s",
                (jlpt_level_id,),
            )

            for topic in data["kanji_topics"]:
                original_id = topic["id"]
                clean_topic = {column: topic.get(column) for column in TOPIC_COLUMNS}
                clean_topic["jlpt_level_id"] = jlpt_level_id
                topic_id_map[original_id] = insert_row(
                    cursor,
                    "kanji_topics",
                    TOPIC_COLUMNS,
                    clean_topic,
                )

            for character in data["kanji_characters"]:
                original_id = character["id"]
                original_topic_id = character["kanji_topic_id"]
                clean_character = {
                    column: character.get(column) for column in CHARACTER_COLUMNS
                }
                clean_character["kanji_topic_id"] = topic_id_map[original_topic_id]
                character_id_map[original_id] = insert_row(
                    cursor,
                    "kanji_characters",
                    CHARACTER_COLUMNS,
                    clean_character,
                )

            for word in data["kanji_words"]:
                original_character_id = word["kanji_character_id"]
                clean_word = {column: word.get(column) for column in WORD_COLUMNS}
                clean_word["kanji_character_id"] = character_id_map[
                    original_character_id
                ]
                insert_row(cursor, "kanji_words", WORD_COLUMNS, clean_word)

            cursor.execute(
                """
                SELECT
                    COUNT(DISTINCT kt.id) AS topics,
                    COUNT(DISTINCT kc.id) AS characters,
                    COUNT(DISTINCT kw.id) AS words
                FROM kanji_topics kt
                LEFT JOIN kanji_characters kc ON kc.kanji_topic_id = kt.id
                LEFT JOIN kanji_words kw ON kw.kanji_character_id = kc.id
                WHERE kt.jlpt_level_id = %s
                """,
                (jlpt_level_id,),
            )
            after = cursor.fetchone()

        connection.commit()
        return {
            "jlpt_level_id": jlpt_level_id,
            "before": before,
            "after": after,
            "dry_run": False,
        }
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Import kanji JSON into MySQL.")
    parser.add_argument("json_path", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    result = import_kanji_json(args.json_path, dry_run=args.dry_run)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
