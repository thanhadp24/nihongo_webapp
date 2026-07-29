SET @schema_name = DATABASE();

SET @has_image_base_path = (
    SELECT COUNT(*)
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = @schema_name
      AND TABLE_NAME = 'visual_resources'
      AND COLUMN_NAME = 'image_base_path'
);
SET @sql = IF(
    @has_image_base_path = 0,
    'ALTER TABLE visual_resources ADD COLUMN image_base_path VARCHAR(1000) NULL AFTER title',
    'SELECT 1'
);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @has_image_filename = (
    SELECT COUNT(*)
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = @schema_name
      AND TABLE_NAME = 'visual_resources'
      AND COLUMN_NAME = 'image_filename'
);
SET @sql = IF(
    @has_image_filename = 0,
    'ALTER TABLE visual_resources ADD COLUMN image_filename VARCHAR(255) NULL AFTER image_base_path',
    'SELECT 1'
);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @has_image_url = (
    SELECT COUNT(*)
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = @schema_name
      AND TABLE_NAME = 'visual_resources'
      AND COLUMN_NAME = 'image_url'
);
SET @sql = IF(
    @has_image_url = 0,
    'SELECT 1',
    'UPDATE visual_resources
     SET image_base_path = COALESCE(
             image_base_path,
             CASE
                 WHEN image_url LIKE ''%/%''
                     THEN LEFT(image_url, LENGTH(image_url) - LOCATE(''/'', REVERSE(image_url)))
                 ELSE ''''
             END
         ),
         image_filename = COALESCE(
             image_filename,
             CASE
                 WHEN image_url LIKE ''%/%''
                     THEN SUBSTRING_INDEX(image_url, ''/'', -1)
                 ELSE image_url
             END
         )'
);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @has_image_url = (
    SELECT COUNT(*)
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = @schema_name
      AND TABLE_NAME = 'visual_resources'
      AND COLUMN_NAME = 'image_url'
);
SET @sql = IF(
    @has_image_url = 0,
    'SELECT 1',
    'ALTER TABLE visual_resources DROP COLUMN image_url'
);
PREPARE stmt FROM @sql;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

ALTER TABLE visual_resources
    MODIFY COLUMN image_base_path VARCHAR(1000) NOT NULL,
    MODIFY COLUMN image_filename VARCHAR(255) NOT NULL;
