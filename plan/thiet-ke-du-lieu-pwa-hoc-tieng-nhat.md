# Thiết kế sản phẩm và dữ liệu cho ứng dụng PWA học tiếng Nhật

## 1. Mục tiêu hệ thống

Ứng dụng PWA học tiếng Nhật dự kiến có các chức năng:

- Học từ vựng theo chủ đề.
- Học ngữ pháp.
- Luyện đọc qua tranh.
- Học từ vựng qua tranh.
- Học câu ví dụ.
- Làm bài tập.
- Lưu từ yêu thích.
- Theo dõi tiến độ học.
- Hoạt động được khi mất mạng.
- Đồng bộ dữ liệu giữa nhiều thiết bị.

Với hệ thống có nhiều chức năng và có khả năng mở rộng trong tương lai, không nên lưu toàn bộ nội dung học tập trong các file JSON tĩnh.

Kiến trúc phù hợp nhất là:

```text
MySQL
  ↓
Backend Python REST API
  ↓
PWA Frontend
  ├── Cache Storage: HTML, CSS, JavaScript, icon, ảnh và tài nguyên tĩnh
  ├── IndexedDB: dữ liệu bài học đã tải để học offline
  └── Sync Queue: lưu các thao tác phát sinh khi mất mạng
```

PWA vẫn là frontend của hệ thống. Backend và cơ sở dữ liệu vẫn được thiết kế như một ứng dụng web thông thường.

### 1.1. Trọng tâm thiết kế hiện tại

Ở giai đoạn đầu, hệ thống nên tập trung vào thiết kế trải nghiệm học và cấu trúc dữ liệu trước. API, đồng bộ offline, tài khoản và trang quản trị sẽ triển khai sau khi luồng dữ liệu học chính đã ổn định.

Ưu tiên hiện tại:

```text
1. Thiết kế luồng học chính
2. Chuẩn hóa dữ liệu cấp độ JLPT
3. Chuẩn hóa dữ liệu chapter theo từng cấp độ
4. Chuẩn hóa dữ liệu chủ đề trong từng chapter
5. Chuẩn hóa dữ liệu từ vựng thuộc từng chủ đề
```

Luồng hiển thị chính của frontend:

```text
Danh sách cấp độ JLPT
  ↓ click một level
Danh sách chapter thuộc level đó
  ↓ trong mỗi chapter
Danh sách chủ đề thuộc chapter đó
  ↓ click một chủ đề
Danh sách từ vựng / bài học thuộc chủ đề
```

Với hướng này, màn hình đầu tiên không cần là trang giới thiệu. Người học nên nhìn thấy ngay các cấp độ JLPT, chọn level và đi tiếp vào chapter/chủ đề.

### 1.2. Mô hình dữ liệu học ưu tiên

Mô hình dữ liệu chính cho giai đoạn đầu:

```text
jlpt_levels
  1-n chapters
        1-n topics
              1-n vocabularies
```

Ý nghĩa:

- Một cấp độ JLPT có nhiều chapter.
- Một chapter thuộc một cấp độ JLPT.
- Một chapter có nhiều chủ đề.
- Một chủ đề thuộc một chapter chính.
- Một chủ đề có nhiều từ vựng.
- Một từ vựng thuộc một chủ đề chính.

Các bảng khác như `grammar_lessons`, `reading_lessons`, `picture_lessons`, `exercises`, `user_progress`, `sync_queue` vẫn quan trọng, nhưng không phải trọng tâm thiết kế đầu tiên.

---

## 2. Vai trò của database, JSON và PWA

### 2.1. Database

Database là nơi lưu dữ liệu gốc của hệ thống.

Database dùng để:

- Quản lý chủ đề.
- Quản lý từ vựng.
- Quản lý ngữ pháp.
- Quản lý bài đọc.
- Quản lý bài tập.
- Quản lý câu hỏi và đáp án.
- Quản lý người dùng.
- Lưu từ yêu thích.
- Lưu lịch sử học.
- Lưu tiến độ học.
- Đồng bộ dữ liệu giữa nhiều thiết bị.
- Cập nhật nội dung qua trang quản trị.

Ví dụ:

```text
topics
vocabularies
grammar_lessons
reading_lessons
picture_lessons
exercises
questions
answers
users
user_favorites
user_progress
```

### 2.2. JSON

JSON chủ yếu là định dạng dữ liệu được truyền giữa backend và frontend.

Ví dụ:

```text
MySQL
  ↓
Backend truy vấn dữ liệu
  ↓
Backend trả về JSON
  ↓
PWA nhận JSON và hiển thị
```

Ví dụ dữ liệu API trả về:

```json
{
  "id": 10,
  "word": "料理",
  "reading": "りょうり",
  "meaning": "nấu ăn",
  "imageUrl": "/media/vocabulary/cooking.webp"
}
```

Như vậy, không phải lựa chọn giữa database và JSON.

Thiết kế đúng là:

```text
Database dùng để lưu dữ liệu
JSON dùng để truyền dữ liệu
IndexedDB dùng để lưu bản sao offline
```

### 2.3. PWA

PWA là ứng dụng frontend có thêm các khả năng:

- Cài đặt lên điện thoại hoặc máy tính.
- Cache tài nguyên.
- Hoạt động một phần khi mất mạng.
- Lưu dữ liệu vào IndexedDB.
- Đồng bộ lại với server khi có mạng.

PWA không thay thế backend hoặc database.

---

## 3. Phân loại dữ liệu trong hệ thống

## 3.1. Dữ liệu nội dung học tập

Nên lưu trong MySQL:

```text
chapters
topics
vocabularies
grammar_lessons
grammar_examples
reading_lessons
reading_pages
picture_lessons
picture_items
exercises
questions
answers
```

Dữ liệu này được backend trả về thông qua API.

Ví dụ:

```http
GET /api/topics
GET /api/topics/5/vocabularies
GET /api/grammar-lessons
GET /api/reading-lessons/12
GET /api/picture-lessons/3
```

## 3.2. Hình ảnh

Không nên lưu trực tiếp dữ liệu ảnh dưới dạng Base64 trong MySQL.

Nên lưu file ảnh tại:

```text
Backend local storage:
media/images/...

Hoặc cloud storage:
Cloudinary
Amazon S3
Google Cloud Storage
```

Trong database chỉ lưu đường dẫn:

```text
/media/vocabulary/kitchen/knife.webp
```

Ví dụ:

```sql
CREATE TABLE media_files (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    file_url VARCHAR(500) NOT NULL,
    file_type VARCHAR(30) NOT NULL,
    alt_text VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## 3.3. Dữ liệu người dùng

Nên lưu trên backend:

```text
users
user_favorites
user_vocabulary_progress
user_grammar_progress
user_reading_history
exercise_attempts
```

Nếu chỉ lưu trong trình duyệt, dữ liệu có thể mất khi:

- Người dùng xóa dữ liệu trình duyệt.
- Người dùng đổi điện thoại.
- Người dùng đăng nhập trên thiết bị khác.
- Người dùng gỡ ứng dụng PWA.

## 3.4. Dữ liệu offline

IndexedDB chỉ nên lưu bản sao của dữ liệu cần học offline.

Ví dụ:

```text
downloaded_topics
downloaded_vocabularies
downloaded_grammar
downloaded_readings
downloaded_picture_lessons
user_progress
sync_queue
metadata
```

Dữ liệu trong IndexedDB không phải nguồn dữ liệu chính.

## 3.5. Cấp độ JLPT

Không nên lưu cấp độ JLPT bằng chuỗi tự do ở nhiều bảng vì dễ phát sinh dữ liệu không thống nhất như `n5`, `N-5`, `N5 `.

Nên tạo bảng chuẩn:

```sql
CREATE TABLE jlpt_levels (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    code VARCHAR(10) NOT NULL,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    display_order INT NOT NULL DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    UNIQUE KEY uk_jlpt_levels_code (code)
);
```

Ví dụ dữ liệu khởi tạo:

```sql
INSERT INTO jlpt_levels (code, name, display_order) VALUES
('N5', 'JLPT N5', 1),
('N4', 'JLPT N4', 2),
('N3', 'JLPT N3', 3),
('N2', 'JLPT N2', 4),
('N1', 'JLPT N1', 5);
```

Các bảng nội dung gắn trực tiếp với cấp độ như `vocabularies`, `grammar_lessons`, `picture_lessons`, `exercise_sets` nên tham chiếu đến `jlpt_levels.id` qua cột `jlpt_level_id`. Riêng `reading_lessons` có thể không cần `jlpt_level_id` nếu là bộ đọc độc lập như `999 lá thư gửi cho chính mình`.

---

## 4. Thiết kế chức năng từ vựng theo chủ đề

Các bảng cơ bản:

```text
chapters
topics
vocabularies
```

Quan hệ dữ liệu học chính là:

```text
Một cấp độ JLPT có nhiều chapter.
Một chapter có nhiều topic.
Một topic có nhiều từ vựng.
```

Nếu sau này cần một từ xuất hiện ở nhiều chủ đề, có thể bổ sung bảng nối sau. Ở giai đoạn hiện tại nên dùng `topic_id` trực tiếp trong bảng `vocabularies` để dữ liệu đơn giản và dễ quản trị hơn.

### 4.1. Bảng chapter

Chapter là nhóm bài học nằm dưới một cấp độ JLPT. Khi người dùng click vào level như `N5`, frontend sẽ load danh sách chapter thuộc level đó.

```sql
CREATE TABLE chapters (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    jlpt_level_id BIGINT NOT NULL,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    display_order INT NOT NULL DEFAULT 0,
    is_published BOOLEAN DEFAULT TRUE,
    version INT NOT NULL DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (jlpt_level_id)
        REFERENCES jlpt_levels(id),

    INDEX idx_chapters_jlpt_level_order (jlpt_level_id, display_order)
);
```

Ví dụ chapter cho `JLPT N5`:

```text
Chapter 1: Chào hỏi và giới thiệu
Chapter 2: Gia đình và đời sống
Chapter 3: Thời gian và lịch trình
Chapter 4: Mua sắm và di chuyển
```

### 4.2. Bảng chủ đề

```sql
CREATE TABLE topics (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    chapter_id BIGINT NOT NULL,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    topic_audio_url VARCHAR(500),
    display_order INT DEFAULT 0,
    is_published BOOLEAN DEFAULT TRUE,
    version INT NOT NULL DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (chapter_id)
        REFERENCES chapters(id),

    INDEX idx_topics_chapter_order (chapter_id, display_order)
);
```

`topic_audio_url` dùng để lưu file audio tổng cho toàn bộ danh sách từ vựng thuộc topic đó.

Ví dụ:

```text
/media/audio/topics/kitchen-vocabulary.mp3
```

Ví dụ chủ đề:

```text
Chào hỏi hằng ngày
Giới thiệu bản thân
Quốc tịch và nghề nghiệp
Thành viên gia đình
Đồ dùng trong nhà
Bữa ăn và thực phẩm
Ngày, tháng, năm
Lịch sinh hoạt
```

### 4.3. Bảng từ vựng

```sql
CREATE TABLE vocabularies (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    topic_id BIGINT NOT NULL,
    word VARCHAR(100) NOT NULL,
    reading VARCHAR(150),
    meaning_vi VARCHAR(500) NOT NULL,
    part_of_speech VARCHAR(50),
    jlpt_level_id BIGINT,
    example_sentence TEXT,
    example_reading TEXT,
    example_meaning_vi TEXT,
    display_order INT DEFAULT 0,
    is_published BOOLEAN DEFAULT TRUE,
    version INT NOT NULL DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (topic_id)
        REFERENCES topics(id),

    FOREIGN KEY (jlpt_level_id)
        REFERENCES jlpt_levels(id)
);
```

Với quan hệ này, frontend có thể load dữ liệu theo thứ tự:

```text
Chọn jlpt_level
  → lấy chapters theo jlpt_level_id
  → lấy topics theo chapter_id
  → lấy vocabularies theo topic_id
```

API `GET /api/topics/{topicId}/vocabularies` chỉ cần lọc theo `vocabularies.topic_id`.

---

## 5. Thiết kế chức năng ngữ pháp

Các bảng chính:

```text
grammar_lessons
grammar_examples
grammar_exercises
```

### 5.1. Bảng bài ngữ pháp

```sql
CREATE TABLE grammar_lessons (
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

    FOREIGN KEY (jlpt_level_id)
        REFERENCES jlpt_levels(id)
);
```

Ví dụ:

```text
Mẫu câu: ～ながら
Ý nghĩa: Vừa làm A vừa làm B
Cấu trúc: Động từ dạng ます bỏ ます + ながら
Cấp độ: N4
```

### 5.2. Bảng ví dụ ngữ pháp

Một bài ngữ pháp có thể có nhiều câu ví dụ, vì vậy nên tách bảng.

```sql
CREATE TABLE grammar_examples (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    grammar_lesson_id BIGINT NOT NULL,
    japanese_text TEXT NOT NULL,
    reading TEXT,
    meaning_vi TEXT,
    display_order INT DEFAULT 0,

    FOREIGN KEY (grammar_lesson_id)
        REFERENCES grammar_lessons(id)
);
```

Ví dụ dữ liệu:

```json
{
  "japaneseText": "音楽を聞きながら勉強します。",
  "reading": "おんがくを ききながら べんきょうします。",
  "meaningVi": "Tôi vừa nghe nhạc vừa học."
}
```

---

## 5.3. Thiết kế chức năng Kanji theo topic

Với chức năng Kanji, luồng học nên đơn giản:

```text
Chọn JLPT level
  ↓
Chọn tab Kanji
  ↓
Danh sách topic Kanji thuộc level đó
  ↓
Chọn topic
  ↓
Học các chữ Kanji và từ Kanji trong topic
```

Với Kanji lấy theo sách như Soumatome, không nên gom quá rộng kiểu `Con người`, `Thời gian`, `Môi trường`.
Mỗi tuần trong sách có nhiều bài nhỏ, nên `kanji_topics` nên bám theo bài/ngày của sách.

Ví dụ N5:

```text
Week 1 Day 1 - お名前は?
Week 1 Day 2 - それは何ですか。
Week 1 Day 3 - 大きい ↔ 小さい
Week 1 Day 4 - どこですか。
Week 1 Day 5 - 何をしていますか。
Week 1 Day 6 - 手と足
Week 2 Day 1 - つめたい飲みもの
Week 2 Day 2 - はたらいています
Week 2 Day 3 - どのぐらい?
Week 2 Day 4 - ちょっと...
Week 2 Day 5 - かぞく
Week 2 Day 6 - すきなもの・ほしいもの
```

UI nên ưu tiên tiếng Nhật:

```text
お名前は?
Tên và giới thiệu bản thân
```

Vì vậy `kanji_topics.name` lưu tên tiếng Nhật chính, còn `kanji_topics.name_vi` lưu phụ đề tiếng Việt.
Các trường `source_week`, `source_day`, `source_page_start` giúp biết topic này đến từ phần nào của sách, nhưng frontend vẫn chỉ cần render theo `level -> topic -> kanji`.

Quan hệ dữ liệu:

```text
jlpt_levels
  1-n kanji_topics
        1-n kanji_characters
              1-n kanji_words
```

### 5.3.1. Bảng topic Kanji

```sql
CREATE TABLE kanji_topics (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    jlpt_level_id BIGINT NOT NULL,
    name VARCHAR(150) NOT NULL,
    name_vi VARCHAR(150),
    description TEXT,
    source_book VARCHAR(150),
    source_week INT,
    source_day INT,
    source_page_start INT,
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
);
```

Ví dụ topic:

```json
{
  "id": 1,
  "jlptLevelId": 1,
  "name": "お名前は?",
  "nameVi": "Tên và giới thiệu bản thân",
  "description": "Bài kanji/vocabulary về tên, người, quốc tịch, trường học và giới thiệu cơ bản.",
  "sourceBook": "Soumatome N5",
  "sourceWeek": 1,
  "sourceDay": 1,
  "sourcePageStart": 16,
  "displayOrder": 1
}
```

### 5.3.2. Bảng chữ Kanji

`han_viet` lưu âm Hán Việt của chữ Kanji. Ví dụ:

```text
森 -> sâm
林 -> lâm
水 -> thủy
火 -> hỏa
```

```sql
CREATE TABLE kanji_characters (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    kanji_topic_id BIGINT NOT NULL,

    character_value VARCHAR(10) NOT NULL,
    han_viet VARCHAR(100),
    onyomi VARCHAR(255),
    kunyomi VARCHAR(255),
    meaning_vi VARCHAR(500) NOT NULL,
    stroke_count INT,

    note TEXT,
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
);
```

Ví dụ:

```json
{
  "id": 1,
  "kanjiTopicId": 1,
  "characterValue": "森",
  "hanViet": "sâm",
  "onyomi": "シン",
  "kunyomi": "もり",
  "meaningVi": "rừng",
  "strokeCount": 12,
  "displayOrder": 1
}
```

### 5.3.3. Bảng từ Kanji

Một chữ Kanji có thể có nhiều từ ví dụ. Bảng này dùng để hiển thị danh sách từ khi người học click vào một Kanji.
`word` là tiếng Nhật chính, `reading` là cách đọc kana/furigana, `meaning_vi` và `example_meaning_vi` là nội dung phụ bên dưới cho người học Việt Nam.

```sql
CREATE TABLE kanji_words (
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
);
```

Ví dụ:

```json
{
  "id": 1,
  "kanjiCharacterId": 1,
  "word": "先生",
  "reading": "せんせい",
  "meaningVi": "giáo viên, thầy cô",
  "exampleSentence": "「先生」をもう一度読みます。",
  "exampleReading": "「せんせい」をもういちどよみます。",
  "exampleMeaningVi": "Tôi đọc lại từ '先生' (giáo viên, thầy cô)."
}
```

API đề xuất:

```http
GET /api/jlpt-levels/{levelId}/kanji-topics
GET /api/kanji-topics/{topicId}/kanji
GET /api/kanji/{kanjiId}/words
```

Response ví dụ:

```json
{
  "topic": {
    "id": 1,
    "name": "お名前は?",
    "nameVi": "Tên và giới thiệu bản thân",
    "sourceWeek": 1,
    "sourceDay": 1,
    "sourcePageStart": 16,
    "jlptLevel": "N5"
  },
  "kanji": [
    {
      "id": 1,
      "characterValue": "先",
      "hanViet": "tiên",
      "onyomi": "セン",
      "kunyomi": "さき",
      "meaningVi": "trước, trước tiên",
      "strokeCount": 6,
      "words": [
        {
          "word": "先生",
          "reading": "せんせい",
          "meaningVi": "giáo viên, thầy cô",
          "exampleSentence": "「先生」をもう一度読みます。",
          "exampleReading": "「せんせい」をもういちどよみます。",
          "exampleMeaningVi": "Tôi đọc lại từ '先生' (giáo viên, thầy cô)."
        }
      ]
    }
  ]
}
```

---

## 6. Thiết kế chức năng luyện đọc qua ảnh

Với bộ `999 lá thư gửi cho chính mình`, mỗi hình ảnh là một bài đọc độc lập. Mỗi bài có thể có một audio riêng, hoặc `NULL` nếu audio chưa chuẩn bị.

Vì vậy không nên gộp nhiều ảnh thành một PDF làm dữ liệu chính. PDF có thể để làm file tải xuống phụ, nhưng UI học nên render theo từng bài ảnh độc lập để dễ next bài, phát audio, lưu tiến độ và đánh dấu yêu thích.

Quan hệ dữ liệu nên là:

```text
reading_collections
  1-n reading_lessons
```

Ý nghĩa:

- `reading_collections` là bộ bài đọc, ví dụ `999 lá thư gửi cho chính mình`.
- `reading_lessons` là từng lá thư/bài đọc độc lập.
- Một bài đọc trong collection hiện tại tương ứng với một ảnh và một audio riêng.
- Thứ tự hiển thị và nút trước/sau của từng lá thư dựa vào `display_order`.

### 6.1. Bảng bộ bài đọc

```sql
CREATE TABLE reading_collections (
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
);
```

Ví dụ:

```json
{
  "id": 1,
  "title": "999 Lá Thư Gửi Cho Chính Mình",
  "slug": "999-la-thu-gui-cho-chinh-minh",
  "description": "Bộ bài đọc truyền động lực luyện dokkai bằng hình ảnh.",
  "coverImageUrl": "/media/readings/999_letters/001.png"
}
```

### 6.2. Bảng bài đọc

```sql
CREATE TABLE reading_lessons (
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

    UNIQUE KEY uk_reading_lessons_collection_order (
        reading_collection_id,
        display_order
    ),

    INDEX idx_reading_lessons_collection_order (
        reading_collection_id,
        display_order
    ),

    FOREIGN KEY (reading_collection_id)
        REFERENCES reading_collections(id)
);
```

Ví dụ một bài:

```json
{
  "id": 1,
  "readingCollectionId": 1,
  "title": "Lá thư 001",
  "imageUrl": "/media/readings/999_letters/001.png",
  "audioUrl": "/media/readings/999_letters/audio/001.mp3",
  "displayOrder": 1
}
```

Nếu audio chưa có:

```json
{
  "id": 2,
  "readingCollectionId": 1,
  "title": "Lá thư 002",
  "imageUrl": "/media/readings/999_letters/002.png",
  "audioUrl": null,
  "displayOrder": 2
}
```

Luồng UI:

```text
Danh sách bộ bài đọc
  ↓ click "999 Lá Thư Gửi Cho Chính Mình"
Danh sách lá thư
  ↓ click một lá thư
Màn đọc:
  - ảnh bài đọc
  - audio player nếu audio_url != null
  - nút Trước / Tiếp theo
  - trạng thái đã đọc / yêu thích
```

API trả về một bài đọc:

```json
{
  "id": 1,
  "title": "Lá thư 001",
  "imageUrl": "/media/readings/999_letters/001.png",
  "audioUrl": "/media/readings/999_letters/audio/001.mp3",
  "displayOrder": 1,
  "nextLessonId": 2,
  "previousLessonId": null
}
```

### 6.3. Bảng tiến độ đọc

Khi có tài khoản, nên lưu trạng thái đọc của từng user theo từng bài.

```sql
CREATE TABLE user_reading_progress (
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

    UNIQUE KEY uk_user_reading_progress (
        user_id,
        reading_lesson_id
    ),

    INDEX idx_user_reading_progress_lesson (reading_lesson_id),

    FOREIGN KEY (reading_lesson_id)
        REFERENCES reading_lessons(id)
);
```

Ở giai đoạn chưa có user, bảng này có thể tạo sẵn nhưng chưa dùng.

### 6.4. Khi nào cần bảng trang đọc?

Chỉ cần thêm bảng `reading_pages` nếu sau này có loại bài đọc mà một bài gồm nhiều trang ảnh.

Ví dụ:

```text
Một bài đọc dài gồm 5 trang scan
Một manga/story gồm nhiều khung ảnh
Một PDF được tách thành nhiều page ảnh để đọc offline
```

Với `999 lá thư gửi cho chính mình`, hiện tại không cần `reading_pages` vì mỗi ảnh đã là một bài độc lập.

---

## 7. Thiết kế chức năng từ vựng qua tranh

Có hai kiểu phổ biến.

## 7.1. Mỗi từ có một ảnh riêng

Trường hợp này chỉ cần lưu đường dẫn ảnh trong bảng `vocabularies`.

Ví dụ:

```json
{
  "word": "包丁",
  "reading": "ほうちょう",
  "meaning": "dao nhà bếp",
  "imageUrl": "/media/vocabulary/kitchen/knife.webp"
}
```

Cách này phù hợp với flashcard hoặc danh sách từ vựng dạng hình ảnh.

## 7.2. Một bức tranh có nhiều từ tương tác

Ví dụ một bức tranh nhà bếp có:

- Tủ lạnh.
- Dao.
- Nồi.
- Chảo.
- Bếp ga.
- Bồn rửa.

Nên dùng:

```text
picture_lessons
picture_items
```

### Bảng bài học qua tranh

```sql
CREATE TABLE picture_lessons (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    image_url VARCHAR(500) NOT NULL,
    jlpt_level_id BIGINT,
    display_order INT DEFAULT 0,
    is_published BOOLEAN DEFAULT TRUE,
    version INT NOT NULL DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (jlpt_level_id)
        REFERENCES jlpt_levels(id)
);
```

### Bảng các vị trí tương tác trên tranh

```sql
CREATE TABLE picture_items (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    picture_lesson_id BIGINT NOT NULL,
    vocabulary_id BIGINT NOT NULL,

    position_x DECIMAL(5,2),
    position_y DECIMAL(5,2),
    width_percent DECIMAL(5,2),
    height_percent DECIMAL(5,2),

    display_order INT DEFAULT 0,

    FOREIGN KEY (picture_lesson_id)
        REFERENCES picture_lessons(id),

    FOREIGN KEY (vocabulary_id)
        REFERENCES vocabularies(id)
);
```

Tọa độ nên lưu theo phần trăm thay vì pixel.

Ví dụ:

```json
{
  "vocabularyId": 101,
  "positionX": 42.5,
  "positionY": 31.8,
  "widthPercent": 10,
  "heightPercent": 12
}
```

Lợi ích của việc dùng phần trăm:

- Ảnh hiển thị đúng trên điện thoại.
- Ảnh hiển thị đúng trên máy tính.
- Vị trí không bị sai khi ảnh thay đổi kích thước.
- Dễ thiết kế vùng có thể nhấn.

---

## 8. Thiết kế câu ví dụ

Một từ có thể có nhiều câu ví dụ. Một câu cũng có thể chứa nhiều từ vựng.

Nên tách thành:

```text
example_sentences
vocabulary_examples
```

### Bảng câu ví dụ

```sql
CREATE TABLE example_sentences (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    sentence TEXT NOT NULL,
    reading TEXT,
    meaning_vi TEXT,
    image_url VARCHAR(500),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
);
```

### Bảng liên kết

```sql
CREATE TABLE vocabulary_examples (
    vocabulary_id BIGINT NOT NULL,
    example_sentence_id BIGINT NOT NULL,
    display_order INT DEFAULT 0,

    PRIMARY KEY (vocabulary_id, example_sentence_id),

    FOREIGN KEY (vocabulary_id)
        REFERENCES vocabularies(id),

    FOREIGN KEY (example_sentence_id)
        REFERENCES example_sentences(id)
);
```

---

## 9. Thiết kế furigana

Có hai cách hiển thị cách đọc.

## 9.1. Lưu toàn bộ câu và toàn bộ cách đọc

Ví dụ:

```json
{
  "sentence": "今日は学校へ行きます。",
  "reading": "きょうは がっこうへ いきます。"
}
```

Phù hợp khi hiển thị cách đọc ở dòng dưới.

## 9.2. Lưu từng đoạn để hiển thị furigana trên Kanji

Ví dụ:

```json
[
  {
    "text": "今日",
    "reading": "きょう"
  },
  {
    "text": "は",
    "reading": null
  },
  {
    "text": "学校",
    "reading": "がっこう"
  },
  {
    "text": "へ",
    "reading": null
  },
  {
    "text": "行",
    "reading": "い"
  },
  {
    "text": "きます。",
    "reading": null
  }
]
```

Có thể lưu dưới dạng JSON trong MySQL:

```sql
ALTER TABLE example_sentences
ADD COLUMN furigana_segments JSON;
```

Frontend có thể render bằng thẻ HTML `ruby` và `rt`.

Ví dụ React:

```jsx
function JapaneseText({ segments }) {
    return (
        <span>
            {segments.map((segment, index) =>
                segment.reading ? (
                    <ruby key={index}>
                        {segment.text}
                        <rt>{segment.reading}</rt>
                    </ruby>
                ) : (
                    <span key={index}>{segment.text}</span>
                )
            )}
        </span>
    );
}
```

---

## 10. Thiết kế bài tập

Các bảng đề xuất:

```text
exercise_sets
exercises
exercise_options
exercise_attempts
exercise_answers
```

### Bảng bộ bài tập

```sql
CREATE TABLE exercise_sets (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    exercise_type VARCHAR(50),
    jlpt_level_id BIGINT,
    thumbnail_url VARCHAR(500),
    is_published BOOLEAN DEFAULT TRUE,
    version INT NOT NULL DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (jlpt_level_id)
        REFERENCES jlpt_levels(id)
);
```

### Bảng câu hỏi

```sql
CREATE TABLE exercises (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    exercise_set_id BIGINT NOT NULL,
    question_type VARCHAR(50) NOT NULL,
    question_text TEXT,
    image_url VARCHAR(500),
    explanation TEXT,
    display_order INT DEFAULT 0,

    FOREIGN KEY (exercise_set_id)
        REFERENCES exercise_sets(id)
);
```

### Bảng lựa chọn

```sql
CREATE TABLE exercise_options (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    exercise_id BIGINT NOT NULL,
    option_text TEXT NOT NULL,
    is_correct BOOLEAN DEFAULT FALSE,
    display_order INT DEFAULT 0,

    FOREIGN KEY (exercise_id)
        REFERENCES exercises(id)
);
```

---

## 11. Dữ liệu tiến độ người dùng

## 11.1. Lưu từ yêu thích

Nếu chỉ cần chức năng bấm tim:

```sql
CREATE TABLE user_saved_vocabularies (
    user_id BIGINT NOT NULL,
    vocabulary_id BIGINT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (user_id, vocabulary_id)
);
```

## 11.2. Theo dõi quá trình học từ vựng

```sql
CREATE TABLE user_vocabulary_progress (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,

    user_id BIGINT NOT NULL,
    vocabulary_id BIGINT NOT NULL,

    is_favorite BOOLEAN NOT NULL DEFAULT FALSE,

    learning_status ENUM(
        'new',
        'learning',
        'reviewing',
        'mastered'
    ) NOT NULL DEFAULT 'new',

    correct_count INT NOT NULL DEFAULT 0,
    incorrect_count INT NOT NULL DEFAULT 0,

    review_interval_days INT NOT NULL DEFAULT 0,
    next_review_at DATETIME,

    version INT NOT NULL DEFAULT 1,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    UNIQUE KEY uk_user_vocabulary (
        user_id,
        vocabulary_id
    )
);
```

## 11.3. Theo dõi lịch sử làm bài

```sql
CREATE TABLE exercise_attempts (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    exercise_set_id BIGINT NOT NULL,
    score DECIMAL(5,2),
    correct_count INT DEFAULT 0,
    total_questions INT DEFAULT 0,
    started_at DATETIME,
    completed_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

---

## 12. IndexedDB trong PWA

IndexedDB nên được dùng để lưu dữ liệu offline.

Các object store đề xuất:

```text
topics
vocabularies
grammar_lessons
reading_lessons
picture_lessons
user_progress
sync_queue
app_metadata
```

## 12.1. Ví dụ dữ liệu từ vựng trong IndexedDB

```json
{
  "id": 1001,
  "word": "今日",
  "reading": "きょう",
  "meaningVi": "hôm nay",
  "jlptLevel": "N5",
  "topicId": 1,
  "imageUrl": "/media/vocabulary/today.webp",
  "version": 2,
  "updatedAt": "2026-07-25T10:30:00Z"
}
```

## 12.2. Ví dụ dữ liệu tiến độ

```json
{
  "key": "12:1001",
  "userId": 12,
  "vocabularyId": 1001,
  "isFavorite": true,
  "learningStatus": "learning",
  "updatedAt": "2026-07-25T10:35:00Z",
  "syncStatus": "pending"
}
```

## 12.3. Sync queue

Khi mất mạng, các thao tác được lưu tạm.

Ví dụ:

```json
{
  "id": "3dd2a97a-2732-47dd-b187-c387cd050d41",
  "entityType": "vocabulary_progress",
  "entityId": "12:1001",
  "operation": "upsert",
  "payload": {
    "vocabularyId": 1001,
    "isFavorite": true
  },
  "createdAt": "2026-07-25T10:35:00Z",
  "retryCount": 0
}
```

Khi có mạng:

```text
1. Đọc dữ liệu trong sync_queue
2. Gửi dữ liệu lên API
3. Backend cập nhật MySQL
4. Nếu thành công thì xóa phần tử khỏi sync_queue
5. Tải các thay đổi mới từ server về
```

---

## 13. Cache Storage

Cache Storage nên dùng cho các tài nguyên tĩnh:

```text
index.html
CSS
JavaScript
font
icon
logo
ảnh giao diện
ảnh bài học đã tải
audio bài nghe đã tải
```

Không nên dùng Cache Storage thay thế database.

Phân chia như sau:

```text
IndexedDB:
- dữ liệu JSON
- nội dung bài học
- tiến độ
- sync queue

Cache Storage:
- HTML
- CSS
- JavaScript
- ảnh
- audio
- icon
```

---

## 14. Cơ chế tải nội dung offline

Không nên tải toàn bộ dữ liệu ngay khi người dùng cài PWA.

Nên cho người dùng chủ động chọn:

```text
Tải chủ đề này để học offline
Tải bài ngữ pháp này
Tải bài đọc này
Tải toàn bộ cấp độ N5
```

Khi tải một chủ đề để học offline, PWA nên tải kèm:

```text
- Dữ liệu topic
- Danh sách từ vựng có topic_id tương ứng
- Ảnh của từng từ vựng
- Audio tổng của topic
```

Luồng hoạt động:

```text
1. Người dùng mở bài học
2. PWA gọi API lấy dữ liệu
3. PWA hiển thị dữ liệu
4. Người dùng chọn “Tải offline”
5. Dữ liệu JSON được lưu vào IndexedDB
6. Ảnh và tài nguyên được lưu vào Cache Storage
7. Khi mất mạng, PWA đọc lại dữ liệu cục bộ
```

Ví dụ dữ liệu lưu offline:

```json
{
  "id": 5,
  "name": "Đồ dùng nhà bếp",
  "topicAudioUrl": "/media/audio/topics/kitchen-vocabulary.mp3",
  "version": 3,
  "downloadedAt": "2026-07-25T05:00:00Z",
  "vocabularies": [
    {
      "id": 101,
      "word": "包丁",
      "reading": "ほうちょう",
      "meaning": "dao nhà bếp",
      "imageUrl": "/media/vocabulary/knife.webp"
    }
  ]
}
```

---

## 15. Cơ chế version và đồng bộ nội dung

Mỗi loại nội dung nên có:

```sql
version INT
updated_at DATETIME
is_published BOOLEAN
```

Ví dụ PWA đang lưu:

```json
{
  "topicId": 5,
  "version": 3
}
```

Server hiện có:

```json
{
  "topicId": 5,
  "version": 4,
  "hasUpdate": true
}
```

PWA chỉ tải lại khi có phiên bản mới.

API kiểm tra cập nhật:

```http
GET /api/content/updates?after=2026-07-25T00:00:00Z
```

Response:

```json
{
  "updatedTopics": [5, 8],
  "updatedGrammarLessons": [12],
  "updatedReadingLessons": [7],
  "deletedItems": [],
  "serverTime": "2026-07-25T06:00:00Z"
}
```

---

## 16. API đề xuất

## 16.1. Chủ đề và từ vựng

```http
GET /api/jlpt-levels
GET /api/jlpt-levels/{levelCode}/chapters
GET /api/chapters/{chapterId}
GET /api/chapters/{chapterId}/topics
GET /api/topics
GET /api/topics/{topicId}
GET /api/topics/{topicId}/vocabularies
GET /api/vocabularies/{vocabularyId}
```

## 16.2. Ngữ pháp

```http
GET /api/grammar-lessons
GET /api/grammar-lessons/{grammarId}
GET /api/grammar-lessons?level=N5
```

## 16.3. Bài đọc

```http
GET /api/reading-lessons
GET /api/reading-lessons/{readingId}
```

## 16.4. Học qua tranh

```http
GET /api/picture-lessons
GET /api/picture-lessons/{pictureLessonId}
```

## 16.5. Tiến độ

```http
GET /api/users/me/progress
POST /api/users/me/vocabulary-progress
POST /api/users/me/exercise-attempts
```

## 16.6. Đồng bộ offline

```http
GET /api/sync?updated_after=2026-07-25T08:00:00Z
POST /api/sync/progress
```

Ví dụ request:

```json
{
  "changes": [
    {
      "clientChangeId": "3dd2a97a-2732-47dd-b187-c387cd050d41",
      "vocabularyId": 1001,
      "isFavorite": true,
      "learningStatus": "learning",
      "clientUpdatedAt": "2026-07-25T10:35:00Z"
    }
  ]
}
```

Response:

```json
{
  "accepted": [
    "3dd2a97a-2732-47dd-b187-c387cd050d41"
  ],
  "serverTime": "2026-07-25T10:40:00Z"
}
```

---

## 17. Dữ liệu nào có thể để trong file JSON tĩnh?

Có thể dùng file JSON cho các dữ liệu nhỏ và ít thay đổi:

```text
Danh sách loại từ
Cấu hình menu
Danh sách ngôn ngữ
Dữ liệu demo
Cấu hình giao diện
```

Ví dụ:

```json
[
  {
    "code": "N5",
    "name": "JLPT N5"
  },
  {
    "code": "N4",
    "name": "JLPT N4"
  },
  {
    "code": "N3",
    "name": "JLPT N3"
  },
  {
    "code": "N2",
    "name": "JLPT N2"
  },
  {
    "code": "N1",
    "name": "JLPT N1"
  }
]
```

Không nên dùng JSON tĩnh cho:

```text
Cấp độ JLPT chính thức của hệ thống
Từ vựng chính
Ngữ pháp
Bài đọc
Bài tập
Dữ liệu người dùng
Tiến độ học
Danh sách yêu thích
Lịch sử làm bài
```

---

## 18. Bảng tổng hợp nơi lưu dữ liệu

| Loại dữ liệu | Nơi lưu chính |
|---|---|
| Cấp độ JLPT | MySQL |
| Chapter theo cấp độ JLPT | MySQL |
| Chủ đề trong chapter | MySQL |
| Từ vựng | MySQL |
| Ngữ pháp | MySQL |
| Bài đọc | MySQL |
| Bài học qua tranh | MySQL |
| Câu hỏi và đáp án | MySQL |
| Người dùng | MySQL |
| Từ yêu thích | MySQL |
| Tiến độ học | MySQL |
| Lịch sử làm bài | MySQL |
| File ảnh | Local storage hoặc cloud storage |
| Đường dẫn ảnh | MySQL |
| File audio tổng của topic | Local storage hoặc cloud storage |
| Đường dẫn audio tổng của topic | MySQL |
| JSON API | Backend tạo từ dữ liệu MySQL |
| Dữ liệu bài học offline | IndexedDB |
| Thao tác chưa đồng bộ | IndexedDB sync_queue |
| HTML, CSS, JS, icon | Cache Storage |
| Ảnh bài học offline | Cache Storage |
| Audio bài học offline | Cache Storage |
| Cấu hình tĩnh nhỏ | File JSON |

---

## 19. Công nghệ đề xuất

### Backend

```text
Python
FastAPI hoặc Flask
SQLAlchemy
MySQL
Alembic
JWT Authentication
```

FastAPI phù hợp khi cần:

- Xây dựng REST API nhanh.
- Tự động tạo tài liệu API.
- Validate dữ liệu bằng Pydantic.
- Dễ mở rộng.
- Hỗ trợ async tốt.

### Frontend PWA

```text
React
Vite
TypeScript
React Router
TanStack Query
Dexie.js
Workbox
```

Trong đó:

- React dùng để xây dựng giao diện.
- Vite dùng để build dự án.
- TanStack Query quản lý dữ liệu API.
- Dexie.js giúp thao tác IndexedDB dễ hơn.
- Workbox hỗ trợ Service Worker và caching.
- React Router quản lý điều hướng.

### Database

```text
MySQL
```

MySQL phù hợp với các quan hệ:

```text
Chủ đề - từ vựng: 1-n
Từ vựng - câu ví dụ
Bài ngữ pháp - ví dụ
Bài đọc - trang đọc
Bài tập - câu hỏi - đáp án
Người dùng - tiến độ
```

### Lưu file

Giai đoạn đầu:

```text
Backend local media folder
```

Khi triển khai thực tế:

```text
Cloudinary
Amazon S3
Google Cloud Storage
```

---

## 20. Cấu trúc thư mục tham khảo

```text
project/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── topics.py
│   │   │   ├── chapters.py
│   │   │   ├── vocabularies.py
│   │   │   ├── grammar.py
│   │   │   ├── readings.py
│   │   │   ├── picture_lessons.py
│   │   │   ├── exercises.py
│   │   │   ├── progress.py
│   │   │   └── sync.py
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── repositories/
│   │   ├── database/
│   │   ├── core/
│   │   └── main.py
│   ├── media/
│   ├── migrations/
│   └── requirements.txt
│
├── frontend/
│   ├── public/
│   │   ├── icons/
│   │   └── manifest.webmanifest
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── features/
│   │   │   ├── vocabulary/
│   │   │   ├── grammar/
│   │   │   ├── reading/
│   │   │   ├── picture-learning/
│   │   │   ├── exercises/
│   │   │   └── offline/
│   │   ├── db/
│   │   │   └── indexedDb.ts
│   │   ├── hooks/
│   │   ├── pages/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── store/
│   │   └── main.tsx
│   └── package.json
│
└── README.md
```

---

## 21. Lộ trình triển khai đề xuất

### Giai đoạn 1: Chốt thiết kế màn hình và dữ liệu học chính

Ưu tiên:

```text
jlpt_levels
chapters
topics
vocabularies
```

Thiết kế màn hình cần có trước:

```text
Màn chọn cấp độ JLPT
Màn danh sách chapter sau khi chọn level
Danh sách chủ đề trong từng chapter
Màn danh sách từ vựng của một chủ đề
```

Mục tiêu của giai đoạn này là người học có thể đi theo luồng:

```text
JLPT level → Chapter → Chủ đề → Từ vựng
```

### Giai đoạn 2: Mở rộng dữ liệu nội dung

Sau khi luồng chính ổn định, bổ sung:

```text
grammar_lessons
grammar_examples
reading_lessons
reading_pages
picture_lessons
picture_items
```

### Giai đoạn 3: Xây dựng API đọc dữ liệu

API ưu tiên:

```text
GET /api/jlpt-levels
GET /api/jlpt-levels/{levelCode}/chapters
GET /api/chapters/{chapterId}/topics
GET /api/topics/{topicId}/vocabularies
```

### Giai đoạn 4: Xây dựng frontend PWA đầy đủ

Tạo các màn hình:

```text
Danh sách cấp độ JLPT
Danh sách chapter theo level
Danh sách chủ đề theo chapter
Danh sách từ vựng
Chi tiết từ vựng
Danh sách ngữ pháp
Chi tiết ngữ pháp
Danh sách bài đọc
Chi tiết bài đọc
Bài học qua tranh
```

### Giai đoạn 5: Thêm tài khoản và tiến độ

Bổ sung:

```text
Đăng ký
Đăng nhập
Từ yêu thích
Tiến độ học
Lịch sử làm bài
```

### Giai đoạn 6: Thêm khả năng offline

Bổ sung:

```text
Service Worker
Cache Storage
IndexedDB
Tải bài học offline
Sync queue
Đồng bộ khi có mạng
```

### Giai đoạn 7: Thêm trang quản trị

Cho phép:

```text
Thêm, sửa, xóa chủ đề
Thêm, sửa, xóa từ vựng
Quản lý ngữ pháp
Quản lý bài đọc
Quản lý bài học qua tranh
Quản lý bài tập
Xuất bản hoặc ẩn nội dung
```

---

## 22. Kết luận

Với ứng dụng PWA học tiếng Nhật có các chức năng như từ vựng theo chủ đề, ngữ pháp, luyện đọc qua tranh và từ vựng qua tranh, nên thiết kế theo hướng:

```text
Backend Python + MySQL là hệ thống chính

PWA Frontend:
- Gọi API lấy dữ liệu JSON
- Cache giao diện và tài nguyên tĩnh
- Lưu bài học tải offline vào IndexedDB
- Lưu ảnh offline vào Cache Storage
- Lưu thao tác offline vào sync_queue
- Đồng bộ với backend khi có mạng
```

Không nên lưu toàn bộ dữ liệu học tập trong các file JSON tĩnh.

File JSON chỉ phù hợp với:

```text
Dữ liệu demo
Cấu hình nhỏ
Danh sách cố định
Dữ liệu ít thay đổi
```

Nội dung chính của ứng dụng vẫn nên được lưu trong database để:

- Dễ quản lý.
- Dễ tìm kiếm.
- Dễ phân trang.
- Dễ cập nhật.
- Dễ xây dựng trang admin.
- Dễ lưu tiến độ.
- Dễ đồng bộ nhiều thiết bị.
- Dễ mở rộng trong tương lai.
