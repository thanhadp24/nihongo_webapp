CREATE TABLE IF NOT EXISTS visual_resource_categories (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    code VARCHAR(50) NOT NULL,
    name_vi VARCHAR(150) NOT NULL,
    description TEXT NULL,
    display_order INT NOT NULL DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    UNIQUE KEY uk_visual_resource_categories_code (code)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS visual_resources (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    category_id BIGINT NOT NULL,
    jlpt_level_id BIGINT NULL,
    title VARCHAR(255) NOT NULL,
    image_base_path VARCHAR(1000) NOT NULL,
    image_filename VARCHAR(255) NOT NULL,
    display_order INT NOT NULL DEFAULT 0,
    is_published BOOLEAN NOT NULL DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    INDEX idx_visual_resources_category (category_id),
    INDEX idx_visual_resources_level (jlpt_level_id),
    INDEX idx_visual_resources_category_level (category_id, jlpt_level_id),

    FOREIGN KEY (category_id)
        REFERENCES visual_resource_categories(id),

    FOREIGN KEY (jlpt_level_id)
        REFERENCES jlpt_levels(id)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

INSERT INTO visual_resource_categories
    (code, name_vi, display_order)
VALUES
    ('reading', 'Đọc hiểu', 1),
    ('vocabulary', 'Từ vựng', 2),
    ('kanji', 'Kanji', 3),
    ('grammar', 'Ngữ pháp', 4),
    ('word_pair', 'Từ đối xứng', 5),
    ('antonym', 'Từ trái nghĩa', 6),
    ('synonym', 'Từ đồng nghĩa', 7),
    ('reduplication', 'Từ láy', 8),
    ('other', 'Khác', 99)
ON DUPLICATE KEY UPDATE
    name_vi = VALUES(name_vi),
    display_order = VALUES(display_order),
    is_active = TRUE;
