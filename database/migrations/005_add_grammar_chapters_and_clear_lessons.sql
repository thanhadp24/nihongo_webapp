DELETE FROM grammar_examples;
DELETE FROM grammar_lessons;

ALTER TABLE grammar_examples AUTO_INCREMENT = 1;
ALTER TABLE grammar_lessons AUTO_INCREMENT = 1;

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

ALTER TABLE grammar_lessons
    DROP INDEX uk_grammar_lessons_level_order,
    ADD COLUMN grammar_chapter_id BIGINT NULL AFTER id;

ALTER TABLE grammar_lessons
    MODIFY grammar_chapter_id BIGINT NOT NULL,
    ADD UNIQUE KEY uk_grammar_lessons_chapter_order (grammar_chapter_id, display_order),
    ADD INDEX idx_grammar_lessons_chapter (grammar_chapter_id),
    ADD CONSTRAINT fk_grammar_lessons_chapter
        FOREIGN KEY (grammar_chapter_id)
        REFERENCES grammar_chapters(id);
