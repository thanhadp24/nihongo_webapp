import os
from typing import Any

from fastapi import Depends, FastAPI, HTTPException, Query, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Connection
from sqlalchemy.exc import SQLAlchemyError

app = FastAPI(title="Nihongo Webapp API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Total-Count"],
)

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    os.environ.get(
        "DATABASE_URL_LOCAL",
        "mysql+pymysql://nihongo:1234@127.0.0.1:13306/nihongo_webapp",
    ),
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)


def get_connection():
    with engine.connect() as connection:
        yield connection


def rows_to_dicts(rows: list[Any]) -> list[dict[str, Any]]:
    return [dict(row._mapping) for row in rows]


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/jlpt-levels")
def list_jlpt_levels(connection: Connection = Depends(get_connection)) -> list[dict[str, Any]]:
    try:
        rows = connection.execute(
            text(
                """
                SELECT
                    jl.id,
                    jl.code,
                    jl.name,
                    jl.description,
                    jl.display_order,
                    COALESCE(vocabulary_counts.total, 0) AS vocabulary_count,
                    COALESCE(kanji_counts.total, 0) AS kanji_count,
                    COALESCE(grammar_counts.total, 0) AS grammar_count
                FROM jlpt_levels jl
                LEFT JOIN (
                    SELECT jlpt_level_id, COUNT(*) AS total
                    FROM vocabularies
                    WHERE is_published = TRUE
                    GROUP BY jlpt_level_id
                ) vocabulary_counts ON vocabulary_counts.jlpt_level_id = jl.id
                LEFT JOIN (
                    SELECT kt.jlpt_level_id, COUNT(kc.id) AS total
                    FROM kanji_topics kt
                    LEFT JOIN kanji_characters kc
                        ON kc.kanji_topic_id = kt.id
                        AND kc.is_published = TRUE
                    WHERE kt.is_published = TRUE
                    GROUP BY kt.jlpt_level_id
                ) kanji_counts ON kanji_counts.jlpt_level_id = jl.id
                LEFT JOIN (
                    SELECT jlpt_level_id, COUNT(*) AS total
                    FROM grammar_lessons
                    WHERE is_published = TRUE
                    GROUP BY jlpt_level_id
                ) grammar_counts ON grammar_counts.jlpt_level_id = jl.id
                WHERE jl.is_active = TRUE
                ORDER BY jl.display_order, jl.id
                """
            )
        ).fetchall()
    except SQLAlchemyError as exc:
        raise HTTPException(status_code=503, detail="Database is unavailable") from exc

    return rows_to_dicts(rows)


@app.get("/api/vocabulary/chapters")
def list_vocabulary_chapters(
    level: str = Query("N5"),
    connection: Connection = Depends(get_connection),
) -> dict[str, Any]:
    try:
        rows = connection.execute(
            text(
                """
                SELECT
                    c.id AS chapter_id,
                    c.chapter_number,
                    c.name AS chapter_name,
                    c.reading AS chapter_reading,
                    c.description AS chapter_description,
                    t.id AS topic_id,
                    t.section_number,
                    t.name AS topic_name,
                    t.description AS topic_description,
                    COUNT(v.id) AS vocabulary_count
                FROM jlpt_levels jl
                JOIN chapters c ON c.jlpt_level_id = jl.id AND c.is_published = TRUE
                LEFT JOIN topics t ON t.chapter_id = c.id AND t.is_published = TRUE
                LEFT JOIN vocabularies v ON v.topic_id = t.id AND v.is_published = TRUE
                WHERE jl.code = :level
                GROUP BY c.id, t.id
                ORDER BY c.display_order, c.chapter_number, t.display_order, t.section_number
                """
            ),
            {"level": level.upper()},
        ).fetchall()
    except SQLAlchemyError as exc:
        raise HTTPException(status_code=503, detail="Database is unavailable") from exc

    chapters: dict[int, dict[str, Any]] = {}
    for row in rows:
        item = row._mapping
        chapter = chapters.setdefault(
            item["chapter_id"],
            {
                "id": item["chapter_id"],
                "chapter_number": item["chapter_number"],
                "name": item["chapter_name"],
                "reading": item["chapter_reading"],
                "description": item["chapter_description"],
                "topics": [],
            },
        )
        if item["topic_id"] is not None:
            chapter["topics"].append(
                {
                    "id": item["topic_id"],
                    "section_number": item["section_number"],
                    "name": item["topic_name"],
                    "description": item["topic_description"],
                    "vocabulary_count": item["vocabulary_count"],
                }
            )

    return {"level": level.upper(), "chapters": list(chapters.values())}


@app.get("/api/vocabularies")
def list_vocabularies(
    response: Response,
    level: str = Query("N5"),
    chapter_id: int | None = None,
    topic_id: int | None = None,
    search: str | None = None,
    limit: int = Query(250, ge=1, le=500),
    offset: int = Query(0, ge=0),
    connection: Connection = Depends(get_connection),
) -> list[dict[str, Any]]:
    filters = ["jl.code = :level", "v.is_published = TRUE"]
    params: dict[str, Any] = {"level": level.upper(), "limit": limit, "offset": offset}

    if chapter_id:
        filters.append("c.id = :chapter_id")
        params["chapter_id"] = chapter_id
    if topic_id:
        filters.append("t.id = :topic_id")
        params["topic_id"] = topic_id
    if search:
        filters.append(
            """
            (
                v.word LIKE :search
                OR v.reading LIKE :search
                OR v.meaning_vi LIKE :search
                OR v.part_of_speech LIKE :search
            )
            """
        )
        params["search"] = f"%{search.strip()}%"

    try:
        total = connection.execute(
            text(
                f"""
                SELECT COUNT(*) AS total
                FROM vocabularies v
                JOIN topics t ON t.id = v.topic_id
                JOIN chapters c ON c.id = t.chapter_id
                JOIN jlpt_levels jl ON jl.id = c.jlpt_level_id
                WHERE {" AND ".join(filters)}
                """
            ),
            params,
        ).scalar_one()
        rows = connection.execute(
            text(
                f"""
                SELECT
                    v.id,
                    v.word,
                    v.reading,
                    v.meaning_vi,
                    v.part_of_speech,
                    v.example_sentence,
                    v.example_reading,
                    v.example_meaning_vi,
                    t.id AS topic_id,
                    t.name AS topic_name,
                    c.id AS chapter_id,
                    c.name AS chapter_name
                FROM vocabularies v
                JOIN topics t ON t.id = v.topic_id
                JOIN chapters c ON c.id = t.chapter_id
                JOIN jlpt_levels jl ON jl.id = c.jlpt_level_id
                WHERE {" AND ".join(filters)}
                ORDER BY c.display_order, t.display_order, v.display_order, v.id
                LIMIT :limit OFFSET :offset
                """
            ),
            params,
        ).fetchall()
    except SQLAlchemyError as exc:
        raise HTTPException(status_code=503, detail="Database is unavailable") from exc

    response.headers["X-Total-Count"] = str(total)
    return rows_to_dicts(rows)


@app.get("/api/kanji/topics")
def list_kanji_topics(
    level: str = Query("N5"),
    connection: Connection = Depends(get_connection),
) -> list[dict[str, Any]]:
    try:
        rows = connection.execute(
            text(
                """
                SELECT
                    kt.id,
                    kt.name,
                    kt.name_reading,
                    kt.name_vi,
                    kt.description,
                    kt.source_book,
                    kt.source_week,
                    kt.source_day,
                    kt.display_order,
                    COUNT(kc.id) AS character_count
                FROM kanji_topics kt
                JOIN jlpt_levels jl ON jl.id = kt.jlpt_level_id
                LEFT JOIN kanji_characters kc
                    ON kc.kanji_topic_id = kt.id
                    AND kc.is_published = TRUE
                WHERE jl.code = :level AND kt.is_published = TRUE
                GROUP BY kt.id
                ORDER BY kt.display_order, kt.id
                """
            ),
            {"level": level.upper()},
        ).fetchall()
    except SQLAlchemyError as exc:
        raise HTTPException(status_code=503, detail="Database is unavailable") from exc

    return rows_to_dicts(rows)


@app.get("/api/kanji/characters")
def list_kanji_characters(
    response: Response,
    level: str = Query("N5"),
    topic_id: int | None = None,
    search: str | None = None,
    limit: int = Query(250, ge=1, le=500),
    offset: int = Query(0, ge=0),
    connection: Connection = Depends(get_connection),
) -> list[dict[str, Any]]:
    filters = ["jl.code = :level", "kc.is_published = TRUE"]
    params: dict[str, Any] = {"level": level.upper(), "limit": limit, "offset": offset}

    if topic_id:
        filters.append("kt.id = :topic_id")
        params["topic_id"] = topic_id
    if search:
        filters.append(
            """
            (
                kc.character_value LIKE :search
                OR kc.han_viet LIKE :search
                OR kc.onyomi LIKE :search
                OR kc.kunyomi LIKE :search
                OR kc.meaning_vi LIKE :search
            )
            """
        )
        params["search"] = f"%{search.strip()}%"

    try:
        total = connection.execute(
            text(
                f"""
                SELECT COUNT(*) AS total
                FROM kanji_characters kc
                JOIN kanji_topics kt ON kt.id = kc.kanji_topic_id
                JOIN jlpt_levels jl ON jl.id = kt.jlpt_level_id
                WHERE {" AND ".join(filters)}
                """
            ),
            params,
        ).scalar_one()
        rows = connection.execute(
            text(
                f"""
                SELECT
                    kc.id,
                    kc.character_value,
                    kc.han_viet,
                    kc.onyomi,
                    kc.kunyomi,
                    kc.meaning_vi,
                    kc.stroke_count,
                    kc.mnemonic_vi,
                    kt.id AS topic_id,
                    kt.name AS topic_name,
                    kt.name_vi AS topic_name_vi
                FROM kanji_characters kc
                JOIN kanji_topics kt ON kt.id = kc.kanji_topic_id
                JOIN jlpt_levels jl ON jl.id = kt.jlpt_level_id
                WHERE {" AND ".join(filters)}
                ORDER BY kt.display_order, kc.display_order, kc.id
                LIMIT :limit OFFSET :offset
                """
            ),
            params,
        ).fetchall()
    except SQLAlchemyError as exc:
        raise HTTPException(status_code=503, detail="Database is unavailable") from exc

    response.headers["X-Total-Count"] = str(total)
    return rows_to_dicts(rows)


@app.get("/api/kanji/characters/{character_id}")
def get_kanji_character(
    character_id: int,
    connection: Connection = Depends(get_connection),
) -> dict[str, Any]:
    try:
        character = connection.execute(
            text(
                """
                SELECT
                    kc.id,
                    kc.character_value,
                    kc.han_viet,
                    kc.onyomi,
                    kc.kunyomi,
                    kc.meaning_vi,
                    kc.stroke_count,
                    kc.mnemonic_vi,
                    kt.id AS topic_id,
                    kt.name AS topic_name,
                    kt.name_vi AS topic_name_vi
                FROM kanji_characters kc
                JOIN kanji_topics kt ON kt.id = kc.kanji_topic_id
                WHERE kc.id = :character_id AND kc.is_published = TRUE
                """
            ),
            {"character_id": character_id},
        ).first()
        if character is None:
            raise HTTPException(status_code=404, detail="Kanji character not found")

        words = connection.execute(
            text(
                """
                SELECT
                    id,
                    word,
                    reading,
                    meaning_vi,
                    example_sentence,
                    example_reading,
                    example_meaning_vi
                FROM kanji_words
                WHERE kanji_character_id = :character_id AND is_published = TRUE
                ORDER BY display_order, id
                """
            ),
            {"character_id": character_id},
        ).fetchall()
    except HTTPException:
        raise
    except SQLAlchemyError as exc:
        raise HTTPException(status_code=503, detail="Database is unavailable") from exc

    payload = dict(character._mapping)
    payload["words"] = rows_to_dicts(words)
    return payload


@app.get("/api/visual-resources")
def list_visual_resources(
    category: str = Query("kanji"),
    level: str | None = None,
    connection: Connection = Depends(get_connection),
) -> list[dict[str, Any]]:
    filters = ["vrc.code = :category", "vr.is_published = TRUE", "vrc.is_active = TRUE"]
    params: dict[str, Any] = {"category": category}

    if level:
        filters.append("jl.code = :level")
        params["level"] = level.upper()

    try:
        rows = connection.execute(
            text(
                f"""
                SELECT
                    vr.id,
                    vrc.code AS category_code,
                    vrc.name_vi AS category_name_vi,
                    jl.code AS jlpt_level_code,
                    vr.title,
                    vr.image_base_path,
                    vr.image_filename,
                    CONCAT(vr.image_base_path, vr.image_filename) AS image_url,
                    vr.display_order
                FROM visual_resources vr
                JOIN visual_resource_categories vrc ON vrc.id = vr.category_id
                LEFT JOIN jlpt_levels jl ON jl.id = vr.jlpt_level_id
                WHERE {" AND ".join(filters)}
                ORDER BY jl.display_order, vr.display_order, vr.id
                """
            ),
            params,
        ).fetchall()
    except SQLAlchemyError as exc:
        raise HTTPException(status_code=503, detail="Database is unavailable") from exc

    return rows_to_dicts(rows)


@app.get("/api/grammar/chapters")
def list_grammar_chapters(
    level: str = Query("N5"),
    connection: Connection = Depends(get_connection),
) -> list[dict[str, Any]]:
    try:
        rows = connection.execute(
            text(
                """
                SELECT
                    gc.id,
                    gc.chapter_number,
                    gc.name,
                    gc.description,
                    gc.display_order,
                    COUNT(gl.id) AS lesson_count
                FROM grammar_chapters gc
                JOIN jlpt_levels jl ON jl.id = gc.jlpt_level_id
                LEFT JOIN grammar_lessons gl
                    ON gl.grammar_chapter_id = gc.id
                    AND gl.is_published = TRUE
                WHERE jl.code = :level AND gc.is_published = TRUE
                GROUP BY gc.id
                ORDER BY gc.display_order, gc.chapter_number, gc.id
                """
            ),
            {"level": level.upper()},
        ).fetchall()
    except SQLAlchemyError as exc:
        raise HTTPException(status_code=503, detail="Database is unavailable") from exc

    return rows_to_dicts(rows)


@app.get("/api/grammar/lessons")
def list_grammar_lessons(
    response: Response,
    level: str = Query("N5"),
    chapter_id: int | None = None,
    search: str | None = None,
    limit: int = Query(250, ge=1, le=500),
    offset: int = Query(0, ge=0),
    connection: Connection = Depends(get_connection),
) -> list[dict[str, Any]]:
    filters = ["jl.code = :level", "gl.is_published = TRUE"]
    params: dict[str, Any] = {"level": level.upper(), "limit": limit, "offset": offset}

    if chapter_id:
        filters.append("gc.id = :chapter_id")
        params["chapter_id"] = chapter_id
    if search:
        filters.append(
            """
            (
                gl.title LIKE :search
                OR gl.pattern LIKE :search
                OR gl.meaning_vi LIKE :search
                OR gl.explanation LIKE :search
            )
            """
        )
        params["search"] = f"%{search.strip()}%"

    try:
        total = connection.execute(
            text(
                f"""
                SELECT COUNT(*) AS total
                FROM grammar_lessons gl
                JOIN grammar_chapters gc ON gc.id = gl.grammar_chapter_id
                JOIN jlpt_levels jl ON jl.id = gl.jlpt_level_id
                WHERE {" AND ".join(filters)}
                """
            ),
            params,
        ).scalar_one()
        rows = connection.execute(
            text(
                f"""
                SELECT
                    gl.id,
                    gl.title,
                    gl.pattern,
                    gl.meaning_vi,
                    gl.explanation,
                    gl.formation,
                    (
                        SELECT ge.japanese_text
                        FROM grammar_examples ge
                        WHERE ge.grammar_lesson_id = gl.id
                        ORDER BY ge.display_order, ge.id
                        LIMIT 1
                    ) AS example_japanese,
                    (
                        SELECT ge.reading
                        FROM grammar_examples ge
                        WHERE ge.grammar_lesson_id = gl.id
                        ORDER BY ge.display_order, ge.id
                        LIMIT 1
                    ) AS example_reading,
                    (
                        SELECT ge.meaning_vi
                        FROM grammar_examples ge
                        WHERE ge.grammar_lesson_id = gl.id
                        ORDER BY ge.display_order, ge.id
                        LIMIT 1
                    ) AS example_meaning_vi,
                    gc.id AS chapter_id,
                    gc.name AS chapter_name,
                    gc.chapter_number
                FROM grammar_lessons gl
                JOIN grammar_chapters gc ON gc.id = gl.grammar_chapter_id
                JOIN jlpt_levels jl ON jl.id = gl.jlpt_level_id
                WHERE {" AND ".join(filters)}
                ORDER BY gc.display_order, gl.display_order, gl.id
                LIMIT :limit OFFSET :offset
                """
            ),
            params,
        ).fetchall()
    except SQLAlchemyError as exc:
        raise HTTPException(status_code=503, detail="Database is unavailable") from exc

    response.headers["X-Total-Count"] = str(total)
    return rows_to_dicts(rows)


@app.get("/api/grammar/lessons/{lesson_id}")
def get_grammar_lesson(
    lesson_id: int,
    connection: Connection = Depends(get_connection),
) -> dict[str, Any]:
    try:
        lesson = connection.execute(
            text(
                """
                SELECT
                    gl.id,
                    gl.title,
                    gl.pattern,
                    gl.meaning_vi,
                    gl.explanation,
                    gl.formation,
                    gc.id AS chapter_id,
                    gc.name AS chapter_name,
                    gc.chapter_number
                FROM grammar_lessons gl
                JOIN grammar_chapters gc ON gc.id = gl.grammar_chapter_id
                WHERE gl.id = :lesson_id AND gl.is_published = TRUE
                """
            ),
            {"lesson_id": lesson_id},
        ).first()
        if lesson is None:
            raise HTTPException(status_code=404, detail="Grammar lesson not found")

        examples = connection.execute(
            text(
                """
                SELECT
                    id,
                    japanese_text,
                    reading,
                    meaning_vi
                FROM grammar_examples
                WHERE grammar_lesson_id = :lesson_id
                ORDER BY display_order, id
                """
            ),
            {"lesson_id": lesson_id},
        ).fetchall()
    except HTTPException:
        raise
    except SQLAlchemyError as exc:
        raise HTTPException(status_code=503, detail="Database is unavailable") from exc

    payload = dict(lesson._mapping)
    payload["examples"] = rows_to_dicts(examples)
    return payload
