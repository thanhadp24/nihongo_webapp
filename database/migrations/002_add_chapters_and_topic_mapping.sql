SET NAMES utf8mb4;

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

ALTER TABLE topics
    ADD COLUMN chapter_id BIGINT NULL AFTER id,
    ADD COLUMN section_number INT NULL AFTER chapter_id;
