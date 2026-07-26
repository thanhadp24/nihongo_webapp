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
