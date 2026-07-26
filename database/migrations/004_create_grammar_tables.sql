CREATE TABLE IF NOT EXISTS grammar_lessons (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
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

    UNIQUE KEY uk_grammar_lessons_level_order (jlpt_level_id, display_order),
    INDEX idx_grammar_lessons_jlpt_level (jlpt_level_id),

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
