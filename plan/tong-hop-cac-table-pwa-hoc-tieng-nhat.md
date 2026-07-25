# Tổng hợp các bảng cho ứng dụng PWA học tiếng Nhật

## 1. Kiến trúc lưu trữ

```text
MySQL (dữ liệu chính)
    ↓ Backend Python REST API trả JSON
PWA frontend
    ├── IndexedDB: dữ liệu bài học tải offline, tiến độ tạm, sync queue
    └── Cache Storage: HTML, CSS, JavaScript, icon, ảnh, audio, font
```

- **MySQL** là nguồn dữ liệu chính.
- **JSON** là định dạng trao đổi dữ liệu giữa backend và PWA.
- **IndexedDB** lưu bản sao cục bộ để học offline.
- **Cache Storage** lưu các file tĩnh.

---

## 2. Danh sách bảng

### 2.1. Người dùng và tài nguyên

| Bảng | Chức năng |
|---|---|
| `users` | Tài khoản người dùng và quản trị viên |
| `media_files` | Thông tin ảnh, audio, video và tài liệu |

### 2.2. Từ vựng và chủ đề

| Bảng | Chức năng |
|---|---|
| `topics` | Chủ đề từ vựng, hỗ trợ chủ đề cha-con |
| `vocabularies` | Nội dung từ vựng |
| `topic_vocabularies` | Liên kết nhiều-nhiều giữa chủ đề và từ vựng |
| `example_sentences` | Kho câu ví dụ dùng chung |
| `vocabulary_examples` | Liên kết từ vựng và câu ví dụ |

### 2.3. Ngữ pháp

| Bảng | Chức năng |
|---|---|
| `grammar_lessons` | Bài học ngữ pháp |
| `grammar_examples` | Ví dụ cho từng bài ngữ pháp |

### 2.4. Luyện đọc qua tranh

| Bảng | Chức năng |
|---|---|
| `reading_lessons` | Thông tin bài đọc |
| `reading_pages` | Trang, cảnh hoặc bức tranh trong bài đọc |
| `reading_vocabulary_notes` | Từ mới và ghi chú của từng trang |

### 2.5. Từ vựng qua tranh

| Bảng | Chức năng |
|---|---|
| `picture_lessons` | Bài học sử dụng một bức tranh lớn |
| `picture_items` | Vùng tương tác và từ vựng trên tranh |

### 2.6. Bài tập

| Bảng | Chức năng |
|---|---|
| `exercise_sets` | Bộ bài tập |
| `exercises` | Câu hỏi trong bộ bài tập |
| `exercise_options` | Các đáp án lựa chọn |
| `topic_exercise_sets` | Gắn bài tập với chủ đề |
| `grammar_exercise_sets` | Gắn bài tập với ngữ pháp |
| `reading_exercise_sets` | Gắn bài tập với bài đọc |
| `picture_exercise_sets` | Gắn bài tập với bài học qua tranh |

### 2.7. Dữ liệu người học

| Bảng | Chức năng |
|---|---|
| `user_saved_vocabularies` | Từ vựng được thả tim |
| `user_vocabulary_progress` | Tiến độ học và ôn từ vựng |
| `user_grammar_progress` | Tiến độ học ngữ pháp |
| `user_reading_progress` | Tiến độ đọc |
| `user_picture_progress` | Tiến độ học qua tranh |
| `exercise_attempts` | Mỗi lần làm một bộ bài tập |
| `exercise_attempt_answers` | Câu trả lời chi tiết của lần làm bài |

### 2.8. Đồng bộ PWA

| Bảng | Chức năng |
|---|---|
| `content_change_logs` | Nhật ký thay đổi nội dung để đồng bộ tăng dần |

Tổng cộng: **29 bảng MySQL**.

---

## 3. Quan hệ tổng thể

```text
topics
  └── topic_vocabularies
        └── vocabularies
              └── vocabulary_examples
                    └── example_sentences

grammar_lessons
  └── grammar_examples

reading_lessons
  └── reading_pages
        └── reading_vocabulary_notes

picture_lessons
  └── picture_items
        └── vocabularies

exercise_sets
  ├── exercises
  │     └── exercise_options
  ├── topic_exercise_sets
  ├── grammar_exercise_sets
  ├── reading_exercise_sets
  └── picture_exercise_sets

users
  ├── user_saved_vocabularies
  ├── user_vocabulary_progress
  ├── user_grammar_progress
  ├── user_reading_progress
  ├── user_picture_progress
  └── exercise_attempts
          └── exercise_attempt_answers
```

---

# 4. SQL tổng hợp

```sql
CREATE DATABASE IF NOT EXISTS japanese_learning
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE japanese_learning;
```

## 4.1. Người dùng

```sql
CREATE TABLE users (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    display_name VARCHAR(150),
    role ENUM('USER', 'ADMIN') NOT NULL DEFAULT 'USER',
    status ENUM('ACTIVE', 'INACTIVE', 'BLOCKED')
        NOT NULL DEFAULT 'ACTIVE',
    last_login_at DATETIME NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_users_email (email)
) ENGINE=InnoDB;
```

## 4.2. File tài nguyên

File thật lưu tại local storage hoặc cloud; database chỉ lưu metadata và URL.

```sql
CREATE TABLE media_files (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    file_name VARCHAR(255) NOT NULL,
    file_key VARCHAR(500) NOT NULL,
    public_url VARCHAR(1000) NOT NULL,
    media_type ENUM('IMAGE', 'AUDIO', 'VIDEO', 'DOCUMENT') NOT NULL,
    mime_type VARCHAR(100),
    storage_provider ENUM('LOCAL', 'CLOUDINARY', 'S3', 'GOOGLE_CLOUD')
        NOT NULL DEFAULT 'LOCAL',
    size_bytes BIGINT UNSIGNED,
    width_px INT UNSIGNED,
    height_px INT UNSIGNED,
    duration_ms INT UNSIGNED,
    alt_text VARCHAR(500),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_media_file_key (file_key),
    INDEX idx_media_type (media_type)
) ENGINE=InnoDB;
```

---

# 5. Từ vựng và chủ đề

## 5.1. Chủ đề

```sql
CREATE TABLE topics (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    parent_id BIGINT UNSIGNED NULL,
    name VARCHAR(150) NOT NULL,
    slug VARCHAR(180) NOT NULL,
    description TEXT,
    thumbnail_media_id BIGINT UNSIGNED NULL,
    display_order INT NOT NULL DEFAULT 0,
    is_published BOOLEAN NOT NULL DEFAULT FALSE,
    version INT UNSIGNED NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME NULL,
    UNIQUE KEY uk_topics_slug (slug),
    CONSTRAINT fk_topics_parent
        FOREIGN KEY (parent_id) REFERENCES topics(id)
        ON DELETE SET NULL,
    CONSTRAINT fk_topics_thumbnail
        FOREIGN KEY (thumbnail_media_id) REFERENCES media_files(id)
        ON DELETE SET NULL,
    INDEX idx_topics_parent (parent_id),
    INDEX idx_topics_published_order (is_published, display_order),
    INDEX idx_topics_updated_at (updated_at)
) ENGINE=InnoDB;
```

## 5.2. Từ vựng

```sql
CREATE TABLE vocabularies (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    word VARCHAR(150) NOT NULL,
    reading VARCHAR(200),
    meaning_vi VARCHAR(1000) NOT NULL,
    part_of_speech VARCHAR(100),
    jlpt_level ENUM('N5', 'N4', 'N3', 'N2', 'N1') NULL,
    note TEXT,
    primary_image_media_id BIGINT UNSIGNED NULL,
    tts_text VARCHAR(500),
    display_order INT NOT NULL DEFAULT 0,
    is_published BOOLEAN NOT NULL DEFAULT FALSE,
    version INT UNSIGNED NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME NULL,
    CONSTRAINT fk_vocabularies_image
        FOREIGN KEY (primary_image_media_id) REFERENCES media_files(id)
        ON DELETE SET NULL,
    INDEX idx_vocabularies_word (word),
    INDEX idx_vocabularies_reading (reading),
    INDEX idx_vocabularies_jlpt (jlpt_level),
    INDEX idx_vocabularies_published (is_published, display_order),
    INDEX idx_vocabularies_updated_at (updated_at)
) ENGINE=InnoDB;
```

## 5.3. Chủ đề – từ vựng

```sql
CREATE TABLE topic_vocabularies (
    topic_id BIGINT UNSIGNED NOT NULL,
    vocabulary_id BIGINT UNSIGNED NOT NULL,
    display_order INT NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (topic_id, vocabulary_id),
    CONSTRAINT fk_topic_vocabularies_topic
        FOREIGN KEY (topic_id) REFERENCES topics(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_topic_vocabularies_vocabulary
        FOREIGN KEY (vocabulary_id) REFERENCES vocabularies(id)
        ON DELETE CASCADE,
    INDEX idx_topic_vocabularies_order (topic_id, display_order),
    INDEX idx_topic_vocabularies_vocabulary (vocabulary_id)
) ENGINE=InnoDB;
```

## 5.4. Câu ví dụ

```sql
CREATE TABLE example_sentences (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    sentence TEXT NOT NULL,
    reading TEXT,
    meaning_vi TEXT,
    furigana_segments JSON NULL,
    image_media_id BIGINT UNSIGNED NULL,
    tts_text TEXT,
    is_published BOOLEAN NOT NULL DEFAULT TRUE,
    version INT UNSIGNED NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME NULL,
    CONSTRAINT fk_example_sentences_image
        FOREIGN KEY (image_media_id) REFERENCES media_files(id)
        ON DELETE SET NULL,
    INDEX idx_example_sentences_updated_at (updated_at)
) ENGINE=InnoDB;
```

## 5.5. Từ vựng – câu ví dụ

```sql
CREATE TABLE vocabulary_examples (
    vocabulary_id BIGINT UNSIGNED NOT NULL,
    example_sentence_id BIGINT UNSIGNED NOT NULL,
    display_order INT NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (vocabulary_id, example_sentence_id),
    CONSTRAINT fk_vocabulary_examples_vocabulary
        FOREIGN KEY (vocabulary_id) REFERENCES vocabularies(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_vocabulary_examples_sentence
        FOREIGN KEY (example_sentence_id) REFERENCES example_sentences(id)
        ON DELETE CASCADE,
    INDEX idx_vocabulary_examples_order (vocabulary_id, display_order)
) ENGINE=InnoDB;
```

---

# 6. Ngữ pháp

## 6.1. Bài ngữ pháp

```sql
CREATE TABLE grammar_lessons (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(280) NOT NULL,
    pattern VARCHAR(500) NOT NULL,
    meaning_vi TEXT,
    explanation LONGTEXT,
    formation TEXT,
    jlpt_level ENUM('N5', 'N4', 'N3', 'N2', 'N1') NULL,
    cover_media_id BIGINT UNSIGNED NULL,
    display_order INT NOT NULL DEFAULT 0,
    is_published BOOLEAN NOT NULL DEFAULT FALSE,
    version INT UNSIGNED NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME NULL,
    UNIQUE KEY uk_grammar_lessons_slug (slug),
    CONSTRAINT fk_grammar_lessons_cover
        FOREIGN KEY (cover_media_id) REFERENCES media_files(id)
        ON DELETE SET NULL,
    INDEX idx_grammar_lessons_jlpt (jlpt_level),
    INDEX idx_grammar_lessons_published (is_published, display_order),
    INDEX idx_grammar_lessons_updated_at (updated_at)
) ENGINE=InnoDB;
```

## 6.2. Ví dụ ngữ pháp

```sql
CREATE TABLE grammar_examples (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    grammar_lesson_id BIGINT UNSIGNED NOT NULL,
    japanese_text TEXT NOT NULL,
    reading TEXT,
    meaning_vi TEXT,
    furigana_segments JSON NULL,
    image_media_id BIGINT UNSIGNED NULL,
    display_order INT NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_grammar_examples_lesson
        FOREIGN KEY (grammar_lesson_id) REFERENCES grammar_lessons(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_grammar_examples_image
        FOREIGN KEY (image_media_id) REFERENCES media_files(id)
        ON DELETE SET NULL,
    INDEX idx_grammar_examples_order (grammar_lesson_id, display_order)
) ENGINE=InnoDB;
```

---

# 7. Luyện đọc qua tranh

## 7.1. Bài đọc

```sql
CREATE TABLE reading_lessons (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(280) NOT NULL,
    description TEXT,
    level ENUM('BEGINNER', 'ELEMENTARY', 'INTERMEDIATE', 'ADVANCED') NULL,
    jlpt_level ENUM('N5', 'N4', 'N3', 'N2', 'N1') NULL,
    thumbnail_media_id BIGINT UNSIGNED NULL,
    estimated_minutes INT UNSIGNED,
    display_order INT NOT NULL DEFAULT 0,
    is_published BOOLEAN NOT NULL DEFAULT FALSE,
    version INT UNSIGNED NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME NULL,
    UNIQUE KEY uk_reading_lessons_slug (slug),
    CONSTRAINT fk_reading_lessons_thumbnail
        FOREIGN KEY (thumbnail_media_id) REFERENCES media_files(id)
        ON DELETE SET NULL,
    INDEX idx_reading_lessons_level (level),
    INDEX idx_reading_lessons_jlpt (jlpt_level),
    INDEX idx_reading_lessons_published (is_published, display_order),
    INDEX idx_reading_lessons_updated_at (updated_at)
) ENGINE=InnoDB;
```

## 7.2. Trang bài đọc

```sql
CREATE TABLE reading_pages (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    reading_lesson_id BIGINT UNSIGNED NOT NULL,
    page_number INT UNSIGNED NOT NULL,
    title VARCHAR(255),
    image_media_id BIGINT UNSIGNED NULL,
    japanese_content LONGTEXT NOT NULL,
    reading_content LONGTEXT,
    meaning_vi LONGTEXT,
    furigana_segments JSON NULL,
    display_order INT NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_reading_page_number (reading_lesson_id, page_number),
    CONSTRAINT fk_reading_pages_lesson
        FOREIGN KEY (reading_lesson_id) REFERENCES reading_lessons(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_reading_pages_image
        FOREIGN KEY (image_media_id) REFERENCES media_files(id)
        ON DELETE SET NULL,
    INDEX idx_reading_pages_order (reading_lesson_id, display_order)
) ENGINE=InnoDB;
```

## 7.3. Từ mới trong bài đọc

```sql
CREATE TABLE reading_vocabulary_notes (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    reading_page_id BIGINT UNSIGNED NOT NULL,
    vocabulary_id BIGINT UNSIGNED NULL,
    word VARCHAR(150) NOT NULL,
    reading VARCHAR(200),
    meaning_vi VARCHAR(1000),
    note TEXT,
    display_order INT NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_reading_vocab_notes_page
        FOREIGN KEY (reading_page_id) REFERENCES reading_pages(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_reading_vocab_notes_vocabulary
        FOREIGN KEY (vocabulary_id) REFERENCES vocabularies(id)
        ON DELETE SET NULL,
    INDEX idx_reading_vocab_notes_order (reading_page_id, display_order)
) ENGINE=InnoDB;
```

---

# 8. Từ vựng qua tranh

## 8.1. Bài học qua tranh

```sql
CREATE TABLE picture_lessons (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(280) NOT NULL,
    description TEXT,
    image_media_id BIGINT UNSIGNED NOT NULL,
    level ENUM('BEGINNER', 'ELEMENTARY', 'INTERMEDIATE', 'ADVANCED') NULL,
    jlpt_level ENUM('N5', 'N4', 'N3', 'N2', 'N1') NULL,
    display_order INT NOT NULL DEFAULT 0,
    is_published BOOLEAN NOT NULL DEFAULT FALSE,
    version INT UNSIGNED NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME NULL,
    UNIQUE KEY uk_picture_lessons_slug (slug),
    CONSTRAINT fk_picture_lessons_image
        FOREIGN KEY (image_media_id) REFERENCES media_files(id),
    INDEX idx_picture_lessons_published (is_published, display_order),
    INDEX idx_picture_lessons_updated_at (updated_at)
) ENGINE=InnoDB;
```

## 8.2. Vùng tương tác trên tranh

Tọa độ được lưu theo phần trăm từ `0` đến `100`, không lưu theo pixel.

```sql
CREATE TABLE picture_items (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    picture_lesson_id BIGINT UNSIGNED NOT NULL,
    vocabulary_id BIGINT UNSIGNED NOT NULL,
    position_x DECIMAL(5,2) NOT NULL,
    position_y DECIMAL(5,2) NOT NULL,
    width_percent DECIMAL(5,2),
    height_percent DECIMAL(5,2),
    display_order INT NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_picture_items_lesson
        FOREIGN KEY (picture_lesson_id) REFERENCES picture_lessons(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_picture_items_vocabulary
        FOREIGN KEY (vocabulary_id) REFERENCES vocabularies(id)
        ON DELETE CASCADE,
    CONSTRAINT chk_picture_items_position_x CHECK (position_x BETWEEN 0 AND 100),
    CONSTRAINT chk_picture_items_position_y CHECK (position_y BETWEEN 0 AND 100),
    CONSTRAINT chk_picture_items_width CHECK (
        width_percent IS NULL OR width_percent BETWEEN 0 AND 100
    ),
    CONSTRAINT chk_picture_items_height CHECK (
        height_percent IS NULL OR height_percent BETWEEN 0 AND 100
    ),
    INDEX idx_picture_items_order (picture_lesson_id, display_order)
) ENGINE=InnoDB;
```

---

# 9. Bài tập

## 9.1. Bộ bài tập

```sql
CREATE TABLE exercise_sets (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(280) NOT NULL,
    description TEXT,
    level ENUM('BEGINNER', 'ELEMENTARY', 'INTERMEDIATE', 'ADVANCED') NULL,
    jlpt_level ENUM('N5', 'N4', 'N3', 'N2', 'N1') NULL,
    thumbnail_media_id BIGINT UNSIGNED NULL,
    time_limit_seconds INT UNSIGNED NULL,
    pass_score DECIMAL(5,2) NOT NULL DEFAULT 60.00,
    display_order INT NOT NULL DEFAULT 0,
    is_published BOOLEAN NOT NULL DEFAULT FALSE,
    version INT UNSIGNED NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME NULL,
    UNIQUE KEY uk_exercise_sets_slug (slug),
    CONSTRAINT fk_exercise_sets_thumbnail
        FOREIGN KEY (thumbnail_media_id) REFERENCES media_files(id)
        ON DELETE SET NULL,
    CONSTRAINT chk_exercise_sets_pass_score CHECK (pass_score BETWEEN 0 AND 100),
    INDEX idx_exercise_sets_published (is_published, display_order),
    INDEX idx_exercise_sets_updated_at (updated_at)
) ENGINE=InnoDB;
```

## 9.2. Câu hỏi

```sql
CREATE TABLE exercises (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    exercise_set_id BIGINT UNSIGNED NOT NULL,
    question_type ENUM(
        'SINGLE_CHOICE',
        'MULTIPLE_CHOICE',
        'TRUE_FALSE',
        'FILL_BLANK',
        'MATCHING',
        'ORDERING',
        'IMAGE_CHOICE'
    ) NOT NULL,
    question_text LONGTEXT,
    question_reading LONGTEXT,
    image_media_id BIGINT UNSIGNED NULL,
    correct_answer_text LONGTEXT,
    answer_data JSON NULL,
    explanation LONGTEXT,
    points DECIMAL(6,2) NOT NULL DEFAULT 1.00,
    display_order INT NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_exercises_set
        FOREIGN KEY (exercise_set_id) REFERENCES exercise_sets(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_exercises_image
        FOREIGN KEY (image_media_id) REFERENCES media_files(id)
        ON DELETE SET NULL,
    INDEX idx_exercises_order (exercise_set_id, display_order)
) ENGINE=InnoDB;
```

## 9.3. Các lựa chọn

```sql
CREATE TABLE exercise_options (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    exercise_id BIGINT UNSIGNED NOT NULL,
    option_text LONGTEXT,
    option_media_id BIGINT UNSIGNED NULL,
    is_correct BOOLEAN NOT NULL DEFAULT FALSE,
    display_order INT NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_exercise_options_exercise
        FOREIGN KEY (exercise_id) REFERENCES exercises(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_exercise_options_media
        FOREIGN KEY (option_media_id) REFERENCES media_files(id)
        ON DELETE SET NULL,
    INDEX idx_exercise_options_order (exercise_id, display_order)
) ENGINE=InnoDB;
```

## 9.4. Các bảng gắn bộ bài tập với nội dung

```sql
CREATE TABLE topic_exercise_sets (
    topic_id BIGINT UNSIGNED NOT NULL,
    exercise_set_id BIGINT UNSIGNED NOT NULL,
    PRIMARY KEY (topic_id, exercise_set_id),
    FOREIGN KEY (topic_id) REFERENCES topics(id) ON DELETE CASCADE,
    FOREIGN KEY (exercise_set_id) REFERENCES exercise_sets(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE grammar_exercise_sets (
    grammar_lesson_id BIGINT UNSIGNED NOT NULL,
    exercise_set_id BIGINT UNSIGNED NOT NULL,
    PRIMARY KEY (grammar_lesson_id, exercise_set_id),
    FOREIGN KEY (grammar_lesson_id) REFERENCES grammar_lessons(id) ON DELETE CASCADE,
    FOREIGN KEY (exercise_set_id) REFERENCES exercise_sets(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE reading_exercise_sets (
    reading_lesson_id BIGINT UNSIGNED NOT NULL,
    exercise_set_id BIGINT UNSIGNED NOT NULL,
    PRIMARY KEY (reading_lesson_id, exercise_set_id),
    FOREIGN KEY (reading_lesson_id) REFERENCES reading_lessons(id) ON DELETE CASCADE,
    FOREIGN KEY (exercise_set_id) REFERENCES exercise_sets(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE picture_exercise_sets (
    picture_lesson_id BIGINT UNSIGNED NOT NULL,
    exercise_set_id BIGINT UNSIGNED NOT NULL,
    PRIMARY KEY (picture_lesson_id, exercise_set_id),
    FOREIGN KEY (picture_lesson_id) REFERENCES picture_lessons(id) ON DELETE CASCADE,
    FOREIGN KEY (exercise_set_id) REFERENCES exercise_sets(id) ON DELETE CASCADE
) ENGINE=InnoDB;
```

---

# 10. Tiến độ người học

## 10.1. Từ được thả tim

```sql
CREATE TABLE user_saved_vocabularies (
    user_id BIGINT UNSIGNED NOT NULL,
    vocabulary_id BIGINT UNSIGNED NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, vocabulary_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (vocabulary_id) REFERENCES vocabularies(id) ON DELETE CASCADE,
    INDEX idx_saved_vocabularies_created_at (user_id, created_at)
) ENGINE=InnoDB;
```

## 10.2. Tiến độ từ vựng

```sql
CREATE TABLE user_vocabulary_progress (
    user_id BIGINT UNSIGNED NOT NULL,
    vocabulary_id BIGINT UNSIGNED NOT NULL,
    learning_status ENUM('NEW', 'LEARNING', 'REVIEWING', 'MASTERED')
        NOT NULL DEFAULT 'NEW',
    correct_count INT UNSIGNED NOT NULL DEFAULT 0,
    incorrect_count INT UNSIGNED NOT NULL DEFAULT 0,
    review_interval_days INT UNSIGNED NOT NULL DEFAULT 0,
    next_review_at DATETIME NULL,
    last_reviewed_at DATETIME NULL,
    version INT UNSIGNED NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, vocabulary_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (vocabulary_id) REFERENCES vocabularies(id) ON DELETE CASCADE,
    INDEX idx_user_vocab_next_review (user_id, next_review_at),
    INDEX idx_user_vocab_status (user_id, learning_status)
) ENGINE=InnoDB;
```

## 10.3. Tiến độ ngữ pháp

```sql
CREATE TABLE user_grammar_progress (
    user_id BIGINT UNSIGNED NOT NULL,
    grammar_lesson_id BIGINT UNSIGNED NOT NULL,
    learning_status ENUM('NOT_STARTED', 'LEARNING', 'COMPLETED')
        NOT NULL DEFAULT 'NOT_STARTED',
    progress_percent DECIMAL(5,2) NOT NULL DEFAULT 0.00,
    last_opened_at DATETIME NULL,
    completed_at DATETIME NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, grammar_lesson_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (grammar_lesson_id) REFERENCES grammar_lessons(id) ON DELETE CASCADE,
    CHECK (progress_percent BETWEEN 0 AND 100),
    INDEX idx_user_grammar_status (user_id, learning_status)
) ENGINE=InnoDB;
```

## 10.4. Tiến độ bài đọc

```sql
CREATE TABLE user_reading_progress (
    user_id BIGINT UNSIGNED NOT NULL,
    reading_lesson_id BIGINT UNSIGNED NOT NULL,
    reading_status ENUM('NOT_STARTED', 'READING', 'COMPLETED')
        NOT NULL DEFAULT 'NOT_STARTED',
    current_page_number INT UNSIGNED NOT NULL DEFAULT 1,
    progress_percent DECIMAL(5,2) NOT NULL DEFAULT 0.00,
    last_opened_at DATETIME NULL,
    completed_at DATETIME NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, reading_lesson_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (reading_lesson_id) REFERENCES reading_lessons(id) ON DELETE CASCADE,
    CHECK (progress_percent BETWEEN 0 AND 100),
    INDEX idx_user_reading_status (user_id, reading_status)
) ENGINE=InnoDB;
```

## 10.5. Tiến độ học qua tranh

```sql
CREATE TABLE user_picture_progress (
    user_id BIGINT UNSIGNED NOT NULL,
    picture_lesson_id BIGINT UNSIGNED NOT NULL,
    learning_status ENUM('NOT_STARTED', 'LEARNING', 'COMPLETED')
        NOT NULL DEFAULT 'NOT_STARTED',
    learned_item_count INT UNSIGNED NOT NULL DEFAULT 0,
    total_item_count INT UNSIGNED NOT NULL DEFAULT 0,
    last_opened_at DATETIME NULL,
    completed_at DATETIME NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, picture_lesson_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (picture_lesson_id) REFERENCES picture_lessons(id) ON DELETE CASCADE,
    INDEX idx_user_picture_status (user_id, learning_status)
) ENGINE=InnoDB;
```

## 10.6. Lần làm bài

```sql
CREATE TABLE exercise_attempts (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT UNSIGNED NOT NULL,
    exercise_set_id BIGINT UNSIGNED NOT NULL,
    attempt_status ENUM('IN_PROGRESS', 'COMPLETED', 'ABANDONED')
        NOT NULL DEFAULT 'IN_PROGRESS',
    score DECIMAL(8,2) NOT NULL DEFAULT 0.00,
    max_score DECIMAL(8,2) NOT NULL DEFAULT 0.00,
    correct_count INT UNSIGNED NOT NULL DEFAULT 0,
    total_questions INT UNSIGNED NOT NULL DEFAULT 0,
    started_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (exercise_set_id) REFERENCES exercise_sets(id) ON DELETE CASCADE,
    INDEX idx_exercise_attempts_user (user_id, started_at),
    INDEX idx_exercise_attempts_set (exercise_set_id, started_at)
) ENGINE=InnoDB;
```

## 10.7. Câu trả lời của lần làm bài

```sql
CREATE TABLE exercise_attempt_answers (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    exercise_attempt_id BIGINT UNSIGNED NOT NULL,
    exercise_id BIGINT UNSIGNED NOT NULL,
    selected_option_ids JSON NULL,
    answer_text LONGTEXT NULL,
    answer_data JSON NULL,
    is_correct BOOLEAN,
    awarded_points DECIMAL(6,2) NOT NULL DEFAULT 0.00,
    answered_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uk_attempt_answer (exercise_attempt_id, exercise_id),
    FOREIGN KEY (exercise_attempt_id) REFERENCES exercise_attempts(id)
        ON DELETE CASCADE,
    FOREIGN KEY (exercise_id) REFERENCES exercises(id)
        ON DELETE CASCADE,
    INDEX idx_attempt_answers_attempt (exercise_attempt_id)
) ENGINE=InnoDB;
```

---

# 11. Nhật ký đồng bộ nội dung

Khi nội dung được thêm, sửa, xóa, xuất bản hoặc ẩn, backend ghi một bản ghi vào bảng này.

```sql
CREATE TABLE content_change_logs (
    id BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    entity_type ENUM(
        'TOPIC',
        'VOCABULARY',
        'EXAMPLE_SENTENCE',
        'GRAMMAR_LESSON',
        'READING_LESSON',
        'READING_PAGE',
        'PICTURE_LESSON',
        'EXERCISE_SET'
    ) NOT NULL,
    entity_id BIGINT UNSIGNED NOT NULL,
    change_action ENUM(
        'CREATED',
        'UPDATED',
        'DELETED',
        'PUBLISHED',
        'UNPUBLISHED'
    ) NOT NULL,
    entity_version INT UNSIGNED NOT NULL DEFAULT 1,
    changed_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_content_changes_time (changed_at),
    INDEX idx_content_changes_entity (entity_type, entity_id)
) ENGINE=InnoDB;
```

---

# 12. Object store trong IndexedDB

Các object store đề xuất:

```text
topics
vocabularies
example_sentences
grammar_lessons
reading_lessons
reading_pages
picture_lessons
exercise_sets
user_progress
sync_queue
app_metadata
```

Ví dụ `sync_queue`:

```json
{
  "id": "client-generated-uuid",
  "entityType": "VOCABULARY_PROGRESS",
  "entityId": "12:1001",
  "operation": "UPSERT",
  "payload": {
    "vocabularyId": 1001,
    "learningStatus": "LEARNING"
  },
  "createdAt": "2026-07-25T10:35:00Z",
  "retryCount": 0
}
```

---

# 13. Dữ liệu trong Cache Storage

```text
index.html
CSS
JavaScript
manifest
icon
font
ảnh giao diện
ảnh bài học đã tải
audio bài học đã tải
```

Không dùng Cache Storage thay thế MySQL hoặc IndexedDB.

---

# 14. Các bảng nên làm trước cho MVP

Không cần tạo cả 29 bảng ngay từ đầu.

## Giai đoạn 1: nội dung chính

```text
users
media_files
topics
vocabularies
topic_vocabularies
example_sentences
vocabulary_examples
grammar_lessons
grammar_examples
reading_lessons
reading_pages
picture_lessons
picture_items
user_saved_vocabularies
```

## Giai đoạn 2: tiến độ

```text
user_vocabulary_progress
user_grammar_progress
user_reading_progress
user_picture_progress
```

## Giai đoạn 3: bài tập

```text
exercise_sets
exercises
exercise_options
topic_exercise_sets
grammar_exercise_sets
reading_exercise_sets
picture_exercise_sets
exercise_attempts
exercise_attempt_answers
```

## Giai đoạn 4: offline và đồng bộ

```text
content_change_logs
IndexedDB
sync_queue
Service Worker
Cache Storage
```

---

# 15. Quy tắc quan trọng

1. Không lưu ảnh Base64 trong MySQL; chỉ lưu file key và URL.
2. Một từ có thể thuộc nhiều chủ đề nên phải dùng `topic_vocabularies`.
3. Một từ có thể có nhiều câu ví dụ nên dùng `vocabulary_examples`.
4. Tọa độ vùng tương tác trên tranh phải lưu theo phần trăm.
5. Nội dung chính nên có `version`, `updated_at`, `deleted_at`, `is_published`.
6. JSON chỉ dùng cho dữ liệu API hoặc cấu trúc linh hoạt như furigana và đáp án phức tạp.
7. Dữ liệu người dùng phải lưu trên server để đồng bộ nhiều thiết bị.
8. IndexedDB chỉ là bản sao offline, không phải nguồn dữ liệu chính.

---

# 16. Kết luận

Thiết kế đầy đủ gồm:

```text
29 bảng MySQL
+
IndexedDB cho dữ liệu offline
+
Cache Storage cho file tĩnh
```

Luồng hoạt động:

```text
MySQL
  ↓
Backend Python API
  ↓ JSON
PWA
  ├── hiển thị dữ liệu trực tuyến
  ├── lưu bài học offline trong IndexedDB
  ├── cache ảnh và file bằng Cache Storage
  └── đồng bộ tiến độ khi có mạng
```
