SET @schema_name = DATABASE();

SET @has_source_name = (
    SELECT COUNT(*)
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = @schema_name
      AND TABLE_NAME = 'reading_collections'
      AND COLUMN_NAME = 'source_name'
);
SET @sql = IF(
    @has_source_name = 0,
    'SELECT 1',
    'ALTER TABLE reading_collections DROP COLUMN source_name'
);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @reading_lessons_jlpt_fk = (
    SELECT CONSTRAINT_NAME
    FROM information_schema.KEY_COLUMN_USAGE
    WHERE TABLE_SCHEMA = @schema_name
      AND TABLE_NAME = 'reading_lessons'
      AND COLUMN_NAME = 'jlpt_level_id'
      AND REFERENCED_TABLE_NAME = 'jlpt_levels'
    LIMIT 1
);
SET @sql = IF(
    @reading_lessons_jlpt_fk IS NULL,
    'SELECT 1',
    CONCAT('ALTER TABLE reading_lessons DROP FOREIGN KEY ', @reading_lessons_jlpt_fk)
);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @has_jlpt_index = (
    SELECT COUNT(*)
    FROM information_schema.STATISTICS
    WHERE TABLE_SCHEMA = @schema_name
      AND TABLE_NAME = 'reading_lessons'
      AND INDEX_NAME = 'idx_reading_lessons_jlpt_level'
);
SET @sql = IF(
    @has_jlpt_index = 0,
    'SELECT 1',
    'ALTER TABLE reading_lessons DROP INDEX idx_reading_lessons_jlpt_level'
);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @has_collection_number_index = (
    SELECT COUNT(*)
    FROM information_schema.STATISTICS
    WHERE TABLE_SCHEMA = @schema_name
      AND TABLE_NAME = 'reading_lessons'
      AND INDEX_NAME = 'uk_reading_lessons_collection_number'
);
SET @sql = IF(
    @has_collection_number_index = 0,
    'SELECT 1',
    'ALTER TABLE reading_lessons DROP INDEX uk_reading_lessons_collection_number'
);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @has_jlpt_level_id = (
    SELECT COUNT(*)
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = @schema_name
      AND TABLE_NAME = 'reading_lessons'
      AND COLUMN_NAME = 'jlpt_level_id'
);
SET @sql = IF(
    @has_jlpt_level_id = 0,
    'SELECT 1',
    'ALTER TABLE reading_lessons DROP COLUMN jlpt_level_id'
);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @has_lesson_number = (
    SELECT COUNT(*)
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = @schema_name
      AND TABLE_NAME = 'reading_lessons'
      AND COLUMN_NAME = 'lesson_number'
);
SET @sql = IF(
    @has_lesson_number = 0,
    'SELECT 1',
    'ALTER TABLE reading_lessons DROP COLUMN lesson_number'
);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @has_image_width = (
    SELECT COUNT(*)
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = @schema_name
      AND TABLE_NAME = 'reading_lessons'
      AND COLUMN_NAME = 'image_width'
);
SET @sql = IF(
    @has_image_width = 0,
    'SELECT 1',
    'ALTER TABLE reading_lessons DROP COLUMN image_width'
);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @has_image_height = (
    SELECT COUNT(*)
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = @schema_name
      AND TABLE_NAME = 'reading_lessons'
      AND COLUMN_NAME = 'image_height'
);
SET @sql = IF(
    @has_image_height = 0,
    'SELECT 1',
    'ALTER TABLE reading_lessons DROP COLUMN image_height'
);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

ALTER TABLE reading_lessons
    MODIFY COLUMN display_order INT NOT NULL DEFAULT 0;

SET @has_collection_order_unique = (
    SELECT COUNT(*)
    FROM information_schema.STATISTICS
    WHERE TABLE_SCHEMA = @schema_name
      AND TABLE_NAME = 'reading_lessons'
      AND INDEX_NAME = 'uk_reading_lessons_collection_order'
);
SET @sql = IF(
    @has_collection_order_unique > 0,
    'SELECT 1',
    'ALTER TABLE reading_lessons ADD UNIQUE KEY uk_reading_lessons_collection_order (reading_collection_id, display_order)'
);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;
