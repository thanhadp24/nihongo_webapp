ALTER TABLE topics
    MODIFY chapter_id BIGINT NOT NULL,
    MODIFY section_number INT NOT NULL,
    ADD UNIQUE KEY uk_topics_chapter_section (chapter_id, section_number),
    ADD INDEX idx_topics_chapter (chapter_id),
    ADD CONSTRAINT fk_topics_chapter
        FOREIGN KEY (chapter_id)
        REFERENCES chapters(id);
