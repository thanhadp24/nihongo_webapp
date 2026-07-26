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
