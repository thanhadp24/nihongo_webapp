# Thiết kế dữ liệu cho ứng dụng PWA học tiếng Nhật

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
    display_order INT DEFAULT 0,
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

Các bảng nội dung như `vocabularies`, `grammar_lessons`, `reading_lessons`, `picture_lessons`, `exercise_sets` nên tham chiếu đến `jlpt_levels.id` qua cột `jlpt_level_id`.

---

## 4. Thiết kế chức năng từ vựng theo chủ đề

Các bảng cơ bản:

```text
topics
vocabularies
topic_vocabularies
```

### 4.1. Bảng chủ đề

```sql
CREATE TABLE topics (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    image_url VARCHAR(500),
    display_order INT DEFAULT 0,
    is_published BOOLEAN DEFAULT TRUE,
    version INT NOT NULL DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
);
```

Ví dụ chủ đề:

```text
Gia đình
Trường học
Đồ dùng nhà bếp
Giao thông
Thời tiết
Du lịch
Công việc
Mua sắm
```

### 4.2. Bảng từ vựng

```sql
CREATE TABLE vocabularies (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    word VARCHAR(100) NOT NULL,
    reading VARCHAR(150),
    meaning_vi VARCHAR(500) NOT NULL,
    part_of_speech VARCHAR(50),
    jlpt_level_id BIGINT,
    image_url VARCHAR(500),
    example_sentence TEXT,
    example_reading TEXT,
    example_meaning_vi TEXT,
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

### 4.3. Bảng liên kết chủ đề và từ vựng

```sql
CREATE TABLE topic_vocabularies (
    topic_id BIGINT NOT NULL,
    vocabulary_id BIGINT NOT NULL,
    display_order INT DEFAULT 0,

    PRIMARY KEY (topic_id, vocabulary_id),

    FOREIGN KEY (topic_id)
        REFERENCES topics(id),

    FOREIGN KEY (vocabulary_id)
        REFERENCES vocabularies(id)
);
```

Nên dùng bảng liên kết vì một từ có thể thuộc nhiều chủ đề.

Ví dụ từ `包丁` có thể thuộc:

```text
Đồ dùng nhà bếp
Nấu ăn
Đồ vật thường ngày
```

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

## 6. Thiết kế chức năng luyện đọc qua tranh

Các bảng đề xuất:

```text
reading_lessons
reading_pages
reading_vocabulary_notes
reading_questions
reading_answers
```

### 6.1. Bảng bài đọc

```sql
CREATE TABLE reading_lessons (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    jlpt_level_id BIGINT,
    thumbnail_url VARCHAR(500),
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

### 6.2. Bảng trang bài đọc

Một bài đọc có thể gồm nhiều trang hoặc nhiều bức tranh.

```sql
CREATE TABLE reading_pages (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    reading_lesson_id BIGINT NOT NULL,
    page_number INT NOT NULL,
    image_url VARCHAR(500),
    japanese_content TEXT NOT NULL,
    reading_content TEXT,
    meaning_vi TEXT,

    FOREIGN KEY (reading_lesson_id)
        REFERENCES reading_lessons(id)
);
```

### 6.3. Bảng ghi chú từ vựng trong bài đọc

```sql
CREATE TABLE reading_vocabulary_notes (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    reading_page_id BIGINT NOT NULL,
    vocabulary_id BIGINT,
    word VARCHAR(100) NOT NULL,
    reading VARCHAR(150),
    meaning_vi VARCHAR(500),
    display_order INT DEFAULT 0,

    FOREIGN KEY (reading_page_id)
        REFERENCES reading_pages(id),

    FOREIGN KEY (vocabulary_id)
        REFERENCES vocabularies(id)
);
```

Bảng này hỗ trợ hiển thị:

- Từ mới trong bài đọc.
- Cách đọc.
- Nghĩa tiếng Việt.
- Liên kết sang màn hình học từ vựng.
- Lưu từ vào danh sách yêu thích.

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
  "topicIds": [1, 3],
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
| Chủ đề | MySQL |
| Cấp độ JLPT | MySQL |
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
| JSON API | Backend tạo từ dữ liệu MySQL |
| Dữ liệu bài học offline | IndexedDB |
| Thao tác chưa đồng bộ | IndexedDB sync_queue |
| HTML, CSS, JS, icon | Cache Storage |
| Ảnh bài học offline | Cache Storage |
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
Chủ đề - từ vựng
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

### Giai đoạn 1: Xây dựng dữ liệu chính

Ưu tiên:

```text
topics
jlpt_levels
vocabularies
grammar_lessons
grammar_examples
reading_lessons
reading_pages
picture_lessons
picture_items
```

Sau đó xây dựng API đọc dữ liệu.

### Giai đoạn 2: Xây dựng frontend PWA

Tạo các màn hình:

```text
Trang chủ
Danh sách chủ đề
Danh sách từ vựng
Chi tiết từ vựng
Danh sách ngữ pháp
Chi tiết ngữ pháp
Danh sách bài đọc
Chi tiết bài đọc
Bài học qua tranh
```

### Giai đoạn 3: Thêm tài khoản và tiến độ

Bổ sung:

```text
Đăng ký
Đăng nhập
Từ yêu thích
Tiến độ học
Lịch sử làm bài
```

### Giai đoạn 4: Thêm khả năng offline

Bổ sung:

```text
Service Worker
Cache Storage
IndexedDB
Tải bài học offline
Sync queue
Đồng bộ khi có mạng
```

### Giai đoạn 5: Thêm trang quản trị

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
