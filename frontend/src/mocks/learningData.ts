import type { Chapter, JLPTLevel, Lesson, Topic, Vocabulary } from "../types/learning";

export const levels: JLPTLevel[] = [
  {
    id: "n5",
    code: "N5",
    name: "JLPT N5",
    subtitle: "Cấp độ nhập môn",
    description: "Dành cho người mới bắt đầu học tiếng Nhật và muốn xây nền thật chắc.",
    chapterCount: 12,
    topicCount: 48,
    vocabularyCount: 650,
    lessonCount: 72,
    progress: 62,
    completedChapters: 7,
    status: "IN_PROGRESS",
    tone: "n5"
  },
  {
    id: "n4",
    code: "N4",
    name: "JLPT N4",
    subtitle: "Giao tiếp cơ bản",
    description: "Mở rộng vốn từ, mẫu câu và kỹ năng đọc hiểu trong đời sống hằng ngày.",
    chapterCount: 14,
    topicCount: 56,
    vocabularyCount: 780,
    lessonCount: 84,
    progress: 28,
    completedChapters: 4,
    status: "IN_PROGRESS",
    tone: "n4"
  },
  {
    id: "n3",
    code: "N3",
    name: "JLPT N3",
    subtitle: "Trung cấp nền tảng",
    description: "Chuẩn bị cho đọc hiểu dài hơn, hội thoại tự nhiên và ngữ pháp đa dạng.",
    chapterCount: 16,
    topicCount: 64,
    vocabularyCount: 980,
    lessonCount: 96,
    progress: 0,
    completedChapters: 0,
    status: "NOT_STARTED",
    tone: "n3"
  },
  {
    id: "n2",
    code: "N2",
    name: "JLPT N2",
    subtitle: "Trung cấp cao",
    description: "Luyện đọc, nghe và diễn đạt trong môi trường học tập, công việc.",
    chapterCount: 18,
    topicCount: 72,
    vocabularyCount: 1200,
    lessonCount: 108,
    progress: 0,
    completedChapters: 0,
    status: "REVIEW_REQUIRED",
    tone: "n2"
  },
  {
    id: "n1",
    code: "N1",
    name: "JLPT N1",
    subtitle: "Nâng cao",
    description: "Chinh phục văn bản học thuật, báo chí và cách diễn đạt tinh tế.",
    chapterCount: 20,
    topicCount: 80,
    vocabularyCount: 1500,
    lessonCount: 120,
    progress: 0,
    completedChapters: 0,
    status: "NOT_STARTED",
    tone: "n1"
  }
];

export const chapters: Chapter[] = [
  {
    id: "n5-c1",
    levelId: "n5",
    chapterNumber: 1,
    title: "Làm quen với tiếng Nhật",
    description: "Học cách chào hỏi, giới thiệu bản thân và sử dụng các câu giao tiếp cơ bản.",
    topicCount: 5,
    vocabularyCount: 68,
    lessonCount: 8,
    progress: 80,
    status: "IN_PROGRESS"
  },
  {
    id: "n5-c2",
    levelId: "n5",
    chapterNumber: 2,
    title: "Gia đình và cuộc sống",
    description: "Học từ vựng và mẫu câu về gia đình, lịch sinh hoạt và đồ dùng quen thuộc.",
    topicCount: 6,
    vocabularyCount: 75,
    lessonCount: 9,
    progress: 100,
    status: "COMPLETED"
  },
  {
    id: "n5-c3",
    levelId: "n5",
    chapterNumber: 3,
    title: "Trường học và công việc",
    description: "Nói về lớp học, nghề nghiệp, lịch làm việc và các hoạt động thường ngày.",
    topicCount: 5,
    vocabularyCount: 72,
    lessonCount: 7,
    progress: 36,
    status: "REVIEW_REQUIRED"
  },
  {
    id: "n5-c4",
    levelId: "n5",
    chapterNumber: 4,
    title: "Ăn uống và mua sắm",
    description: "Gọi món, hỏi giá, diễn đạt sở thích và nói về món ăn Nhật Bản.",
    topicCount: 4,
    vocabularyCount: 64,
    lessonCount: 6,
    progress: 0,
    status: "NOT_STARTED"
  },
  {
    id: "n4-c1",
    levelId: "n4",
    chapterNumber: 1,
    title: "Kể chuyện hằng ngày",
    description: "Dùng thể quá khứ, liên kết câu và kể lại trải nghiệm ngắn.",
    topicCount: 5,
    vocabularyCount: 82,
    lessonCount: 8,
    progress: 45,
    status: "IN_PROGRESS"
  },
  {
    id: "n4-c2",
    levelId: "n4",
    chapterNumber: 2,
    title: "Di chuyển trong thành phố",
    description: "Hỏi đường, đi tàu điện, đặt lịch hẹn và mô tả địa điểm.",
    topicCount: 5,
    vocabularyCount: 79,
    lessonCount: 8,
    progress: 0,
    status: "NOT_STARTED"
  }
];

export const topics: Topic[] = [
  {
    id: "n5-c1-t1",
    levelId: "n5",
    chapterId: "n5-c1",
    topicNumber: 1,
    title: "Chào hỏi cơ bản",
    japaneseTitle: "あいさつ",
    description: "Các cách chào hỏi thông dụng trong đời sống hằng ngày.",
    vocabularyCount: 15,
    lessonCount: 2,
    exerciseCount: 1,
    progress: 75,
    status: "IN_PROGRESS",
    illustration: "greetings"
  },
  {
    id: "n5-c1-t2",
    levelId: "n5",
    chapterId: "n5-c1",
    topicNumber: 2,
    title: "Giới thiệu bản thân",
    japaneseTitle: "じこしょうかい",
    description: "Nói tên, quốc tịch, nghề nghiệp và sở thích một cách tự nhiên.",
    vocabularyCount: 18,
    lessonCount: 2,
    exerciseCount: 1,
    progress: 60,
    status: "IN_PROGRESS",
    illustration: "profile"
  },
  {
    id: "n5-c1-t3",
    levelId: "n5",
    chapterId: "n5-c1",
    topicNumber: 3,
    title: "Quốc gia và nghề nghiệp",
    japaneseTitle: "くにとしごと",
    description: "Học tên quốc gia, nghề nghiệp và cách hỏi thông tin cơ bản.",
    vocabularyCount: 20,
    lessonCount: 3,
    exerciseCount: 2,
    progress: 20,
    status: "NOT_STARTED",
    illustration: "world"
  },
  {
    id: "n5-c2-t1",
    levelId: "n5",
    chapterId: "n5-c2",
    topicNumber: 1,
    title: "Gia đình",
    japaneseTitle: "かぞく",
    description: "Gọi tên thành viên gia đình và giới thiệu người thân.",
    vocabularyCount: 16,
    lessonCount: 2,
    exerciseCount: 1,
    progress: 100,
    status: "COMPLETED",
    illustration: "home"
  },
  {
    id: "n4-c1-t1",
    levelId: "n4",
    chapterId: "n4-c1",
    topicNumber: 1,
    title: "Kể lại cuối tuần",
    japaneseTitle: "しゅうまつ",
    description: "Kể lại hoạt động cuối tuần bằng câu nối đơn giản.",
    vocabularyCount: 22,
    lessonCount: 3,
    exerciseCount: 1,
    progress: 45,
    status: "IN_PROGRESS",
    illustration: "calendar"
  }
];

export const vocabularies: Vocabulary[] = [
  {
    id: "v-ohayo",
    topicId: "n5-c1-t1",
    word: "おはよう",
    reading: "おはよう",
    romaji: "ohayou",
    meaning: "Chào buổi sáng",
    partOfSpeech: "Cụm chào hỏi",
    example: "おはようございます。",
    exampleMeaning: "Chào buổi sáng ạ.",
    status: "COMPLETED",
    saved: true
  },
  {
    id: "v-konnichiwa",
    topicId: "n5-c1-t1",
    word: "こんにちは",
    reading: "こんにちは",
    romaji: "konnichiwa",
    meaning: "Xin chào",
    partOfSpeech: "Cụm chào hỏi",
    example: "こんにちは、田中さん。",
    exampleMeaning: "Xin chào, anh Tanaka.",
    status: "IN_PROGRESS",
    saved: false
  },
  {
    id: "v-konbanwa",
    topicId: "n5-c1-t1",
    word: "こんばんは",
    reading: "こんばんは",
    romaji: "konbanwa",
    meaning: "Chào buổi tối",
    partOfSpeech: "Cụm chào hỏi",
    example: "こんばんは。またあした。",
    exampleMeaning: "Chào buổi tối. Hẹn gặp lại ngày mai.",
    status: "REVIEW_REQUIRED",
    saved: false
  },
  {
    id: "v-watashi",
    topicId: "n5-c1-t2",
    word: "私",
    reading: "わたし",
    romaji: "watashi",
    meaning: "Tôi",
    partOfSpeech: "Đại từ",
    example: "私はベトナム人です。",
    exampleMeaning: "Tôi là người Việt Nam.",
    status: "IN_PROGRESS",
    saved: true
  },
  {
    id: "v-gakusei",
    topicId: "n5-c1-t2",
    word: "学生",
    reading: "がくせい",
    romaji: "gakusei",
    meaning: "Học sinh, sinh viên",
    partOfSpeech: "Danh từ",
    example: "私は学生です。",
    exampleMeaning: "Tôi là học sinh/sinh viên.",
    status: "NOT_STARTED",
    saved: false
  }
];

export const lessons: Lesson[] = [
  {
    id: "lesson-greetings-1",
    topicId: "n5-c1-t1",
    lessonNumber: 1,
    title: "Cách chào hỏi vào buổi sáng",
    japaneseTitle: "朝のあいさつ",
    type: "DIALOGUE",
    durationMinutes: 8,
    vocabularyCount: 12,
    patternCount: 2,
    progress: 60,
    status: "IN_PROGRESS"
  },
  {
    id: "lesson-greetings-2",
    topicId: "n5-c1-t1",
    lessonNumber: 2,
    title: "Chào hỏi lịch sự",
    japaneseTitle: "ていねいなあいさつ",
    type: "GRAMMAR",
    durationMinutes: 10,
    vocabularyCount: 10,
    patternCount: 3,
    progress: 0,
    status: "NOT_STARTED"
  },
  {
    id: "lesson-intro-1",
    topicId: "n5-c1-t2",
    lessonNumber: 1,
    title: "Nói tên và quốc tịch",
    japaneseTitle: "名前と国",
    type: "DIALOGUE",
    durationMinutes: 9,
    vocabularyCount: 14,
    patternCount: 2,
    progress: 40,
    status: "IN_PROGRESS"
  }
];
