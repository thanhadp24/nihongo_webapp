CREATE TABLE IF NOT EXISTS jlpt_levels (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    code VARCHAR(10) NOT NULL,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    display_order INT NOT NULL DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_jlpt_levels_code (code)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS chapters (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    jlpt_level_id BIGINT NOT NULL,
    chapter_number INT NOT NULL,
    name VARCHAR(150) NOT NULL,
    reading VARCHAR(150),
    description TEXT,
    display_order INT DEFAULT 0,
    is_published BOOLEAN DEFAULT TRUE,
    version INT NOT NULL DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    UNIQUE KEY uk_chapters_level_number (jlpt_level_id, chapter_number),
    INDEX idx_chapters_jlpt_level (jlpt_level_id),

    FOREIGN KEY (jlpt_level_id)
        REFERENCES jlpt_levels(id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS topics (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    chapter_id BIGINT NOT NULL,
    section_number INT NOT NULL,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    topic_audio_url VARCHAR(500),
    display_order INT DEFAULT 0,
    is_published BOOLEAN DEFAULT TRUE,
    version INT NOT NULL DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    UNIQUE KEY uk_topics_chapter_section (chapter_id, section_number),
    INDEX idx_topics_chapter (chapter_id),

    FOREIGN KEY (chapter_id)
        REFERENCES chapters(id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS vocabularies (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    topic_id BIGINT NOT NULL,
    word VARCHAR(100) NOT NULL,
    reading VARCHAR(150),
    meaning_vi VARCHAR(500) NOT NULL,
    part_of_speech VARCHAR(50),
    jlpt_level_id BIGINT,
    example_sentence TEXT,
    example_reading TEXT,
    example_meaning_vi TEXT,
    display_order INT DEFAULT 0,
    is_published BOOLEAN DEFAULT TRUE,
    version INT NOT NULL DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    UNIQUE KEY uk_vocabularies_topic_order (topic_id, display_order),
    INDEX idx_vocabularies_jlpt_level (jlpt_level_id),

    FOREIGN KEY (topic_id)
        REFERENCES topics(id),

    FOREIGN KEY (jlpt_level_id)
        REFERENCES jlpt_levels(id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS kanji_topics (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    jlpt_level_id BIGINT NOT NULL,
    name VARCHAR(150) NOT NULL,
    name_reading VARCHAR(150),
    name_vi VARCHAR(150),
    description TEXT,
    source_book VARCHAR(150),
    source_week INT,
    source_week_title VARCHAR(150),
    source_week_title_vi VARCHAR(150),
    source_day INT,
    source_page_start INT,
    source_url VARCHAR(500),
    display_order INT NOT NULL DEFAULT 0,
    is_published BOOLEAN DEFAULT TRUE,
    version INT NOT NULL DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    UNIQUE KEY uk_kanji_topics_level_order (
        jlpt_level_id,
        display_order
    ),

    INDEX idx_kanji_topics_level (
        jlpt_level_id
    ),

    FOREIGN KEY (jlpt_level_id)
        REFERENCES jlpt_levels(id)
        ON DELETE CASCADE
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS kanji_characters (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    kanji_topic_id BIGINT NOT NULL,
    character_value VARCHAR(10) NOT NULL,
    han_viet VARCHAR(100),
    onyomi VARCHAR(255),
    kunyomi VARCHAR(255),
    meaning_vi VARCHAR(500) NOT NULL,
    stroke_count INT,
    mnemonic_vi TEXT,
    display_order INT NOT NULL DEFAULT 0,
    is_published BOOLEAN DEFAULT TRUE,
    version INT NOT NULL DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    UNIQUE KEY uk_kanji_characters_topic_value (
        kanji_topic_id,
        character_value
    ),

    UNIQUE KEY uk_kanji_characters_topic_order (
        kanji_topic_id,
        display_order
    ),

    INDEX idx_kanji_characters_topic_order (
        kanji_topic_id,
        display_order
    ),

    FOREIGN KEY (kanji_topic_id)
        REFERENCES kanji_topics(id)
        ON DELETE CASCADE
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS kanji_words (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    kanji_character_id BIGINT NOT NULL,
    word VARCHAR(100) NOT NULL,
    reading VARCHAR(150),
    meaning_vi VARCHAR(500) NOT NULL,
    example_sentence TEXT,
    example_reading TEXT,
    example_meaning_vi TEXT,
    display_order INT NOT NULL DEFAULT 0,
    is_published BOOLEAN DEFAULT TRUE,
    version INT NOT NULL DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    UNIQUE KEY uk_kanji_words_character_order (
        kanji_character_id,
        display_order
    ),

    INDEX idx_kanji_words_character (
        kanji_character_id
    ),

    FOREIGN KEY (kanji_character_id)
        REFERENCES kanji_characters(id)
        ON DELETE CASCADE
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS grammar_chapters (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    jlpt_level_id BIGINT NOT NULL,
    chapter_number INT NOT NULL,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    display_order INT DEFAULT 0,
    is_published BOOLEAN DEFAULT TRUE,
    version INT NOT NULL DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    UNIQUE KEY uk_grammar_chapters_level_number (jlpt_level_id, chapter_number),
    INDEX idx_grammar_chapters_jlpt_level (jlpt_level_id),

    FOREIGN KEY (jlpt_level_id)
        REFERENCES jlpt_levels(id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS grammar_lessons (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    grammar_chapter_id BIGINT NOT NULL,
    title VARCHAR(255) NOT NULL,
    pattern VARCHAR(255) NOT NULL,
    meaning_vi TEXT,
    explanation TEXT,
    formation TEXT,
    jlpt_level_id BIGINT,
    display_order INT DEFAULT 0,
    is_published BOOLEAN DEFAULT TRUE,
    version INT NOT NULL DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    UNIQUE KEY uk_grammar_lessons_chapter_order (grammar_chapter_id, display_order),
    INDEX idx_grammar_lessons_chapter (grammar_chapter_id),
    INDEX idx_grammar_lessons_jlpt_level (jlpt_level_id),

    FOREIGN KEY (grammar_chapter_id)
        REFERENCES grammar_chapters(id),

    FOREIGN KEY (jlpt_level_id)
        REFERENCES jlpt_levels(id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS grammar_examples (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    grammar_lesson_id BIGINT NOT NULL,
    japanese_text TEXT NOT NULL,
    reading TEXT,
    meaning_vi TEXT,
    display_order INT DEFAULT 0,

    INDEX idx_grammar_examples_lesson (grammar_lesson_id),

    FOREIGN KEY (grammar_lesson_id)
        REFERENCES grammar_lessons(id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS reading_collections (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(180) NOT NULL,
    description TEXT,
    cover_image_url VARCHAR(500),
    display_order INT DEFAULT 0,
    is_published BOOLEAN DEFAULT TRUE,
    version INT NOT NULL DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    UNIQUE KEY uk_reading_collections_slug (slug)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS reading_lessons (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    reading_collection_id BIGINT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    image_url VARCHAR(500) NOT NULL,
    audio_url VARCHAR(500),
    display_order INT NOT NULL DEFAULT 0,
    is_published BOOLEAN DEFAULT TRUE,
    version INT NOT NULL DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    UNIQUE KEY uk_reading_lessons_collection_order (reading_collection_id, display_order),
    INDEX idx_reading_lessons_collection_order (reading_collection_id, display_order),

    FOREIGN KEY (reading_collection_id)
        REFERENCES reading_collections(id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS user_reading_progress (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    reading_lesson_id BIGINT NOT NULL,
    is_favorite BOOLEAN NOT NULL DEFAULT FALSE,
    is_completed BOOLEAN NOT NULL DEFAULT FALSE,
    last_read_at DATETIME,
    completed_at DATETIME,
    version INT NOT NULL DEFAULT 1,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    UNIQUE KEY uk_user_reading_progress (user_id, reading_lesson_id),
    INDEX idx_user_reading_progress_lesson (reading_lesson_id),

    FOREIGN KEY (reading_lesson_id)
        REFERENCES reading_lessons(id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
