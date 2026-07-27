import { api } from "../api";
import type {
  GrammarDetail,
  GrammarLesson,
  JlptLevel,
  KanjiCharacter,
  KanjiTopic,
  VocabularyChapter,
  VocabularyItem,
  VocabularyTopic
} from "../types";
import type {
  Chapter,
  FlashcardItem,
  JLPTLevel,
  Kanji,
  KanjiTopicSummary,
  Lesson,
  Topic,
  Vocabulary
} from "../types/learning";

type PageRequest = {
  page?: number;
  pageSize?: number;
  search?: string;
};

type PaginatedLearningResult<T> = {
  items: T[];
  total: number;
  page: number;
  pageSize: number;
};

function normalizePage({ page = 1, pageSize = 24 }: PageRequest = {}) {
  const safePage = Math.max(1, page);
  const safePageSize = Math.min(500, Math.max(1, pageSize));

  return {
    page: safePage,
    pageSize: safePageSize,
    offset: (safePage - 1) * safePageSize
  };
}

async function collectAllPages<T>(
  loader: (page: number) => Promise<PaginatedLearningResult<T>>
) {
  const first = await loader(1);
  const totalPages = Math.max(1, Math.ceil(first.total / first.pageSize));

  if (totalPages === 1) return first.items;

  const rest = await Promise.all(
    Array.from({ length: totalPages - 1 }, (_, index) => loader(index + 2))
  );

  return [...first.items, ...rest.flatMap((page) => page.items)];
}

function levelCodeFromId(levelId: string) {
  return levelId.toUpperCase();
}

function levelIdFromCode(code: string) {
  return code.toLowerCase();
}

function toneFromCode(code: string): JLPTLevel["tone"] {
  return levelIdFromCode(code) as JLPTLevel["tone"];
}

function reviewProgress(code: string) {
  if (["N5", "N4", "N3"].includes(code)) return 100;
  if (code === "N2") return 70;
  return 0;
}

function reviewStatus(code: string): JLPTLevel["status"] {
  if (["N5", "N4", "N3"].includes(code)) return "COMPLETED";
  if (code === "N2") return "REVIEW_REQUIRED";
  return "NOT_STARTED";
}

function mapLevel(level: JlptLevel, chapters: VocabularyChapter[] = []): JLPTLevel {
  const topicCount = chapters.reduce((total, chapter) => total + chapter.topics.length, 0);

  return {
    id: levelIdFromCode(level.code),
    code: level.code,
    name: level.name || `JLPT ${level.code}`,
    subtitle: level.description || "Mở để ôn tập",
    description:
      level.description ||
      `Ôn tập từ vựng, Kanji và ngữ pháp theo dữ liệu ${level.code} trong hệ thống.`,
    chapterCount: chapters.length,
    topicCount,
    vocabularyCount: level.vocabulary_count,
    lessonCount: level.grammar_count,
    progress: reviewProgress(level.code),
    completedChapters: level.code === "N2" ? 0 : chapters.length,
    status: reviewStatus(level.code),
    tone: toneFromCode(level.code)
  };
}

function mapChapter(levelId: string, chapter: VocabularyChapter, index: number): Chapter {
  const vocabularyCount = chapter.topics.reduce((total, topic) => total + topic.vocabulary_count, 0);

  return {
    id: String(chapter.id),
    levelId,
    chapterNumber: chapter.chapter_number ?? index + 1,
    title: chapter.name,
    description: chapter.description || chapter.reading || "Nội dung ôn tập theo chapter.",
    topicCount: chapter.topics.length,
    vocabularyCount,
    lessonCount: 0,
    progress: 0,
    status: "REVIEW_REQUIRED"
  };
}

function mapTopic(levelId: string, chapterId: string, topic: VocabularyTopic): Topic {
  return {
    id: String(topic.id),
    levelId,
    chapterId,
    topicNumber: topic.section_number,
    title: topic.name,
    japaneseTitle: topic.name,
    description: topic.description || "Ôn tập từ vựng thuộc chủ đề này.",
    vocabularyCount: topic.vocabulary_count,
    lessonCount: 0,
    exerciseCount: 0,
    progress: 0,
    status: "REVIEW_REQUIRED",
    illustration: "greetings"
  };
}

function mapVocabulary(item: VocabularyItem): Vocabulary {
  return {
    id: String(item.id),
    topicId: String(item.topic_id),
    word: item.word,
    reading: item.reading || item.word,
    romaji: item.reading || "",
    meaning: item.meaning_vi,
    partOfSpeech: item.part_of_speech || "Từ vựng",
    example: item.example_sentence || "",
    exampleMeaning: item.example_meaning_vi || "",
    status: "REVIEW_REQUIRED",
    saved: false
  };
}

function mapKanji(item: KanjiCharacter): Kanji {
  return {
    id: String(item.id),
    topicId: String(item.topic_id),
    character: item.character_value,
    hanViet: item.han_viet || "",
    onyomi: item.onyomi || "",
    kunyomi: item.kunyomi || "",
    meaning: item.meaning_vi,
    strokeCount: item.stroke_count,
    mnemonic: item.mnemonic_vi || "",
    topicName: item.topic_name,
    topicMeaning: item.topic_name_vi || "",
    status: "REVIEW_REQUIRED",
    saved: false
  };
}

function mapKanjiTopic(topic: KanjiTopic): KanjiTopicSummary {
  return {
    id: String(topic.id),
    title: topic.name,
    reading: topic.name_reading || "",
    meaning: topic.name_vi || "",
    description: topic.description || "",
    characterCount: topic.character_count
  };
}

function mapGrammarLesson(lesson: GrammarLesson): Lesson {
  return {
    id: String(lesson.id),
    topicId: String(lesson.chapter_id),
    lessonNumber: lesson.id,
    title: lesson.title || lesson.pattern,
    japaneseTitle: lesson.pattern,
    type: "GRAMMAR",
    durationMinutes: 8,
    vocabularyCount: 0,
    patternCount: 1,
    progress: 0,
    status: "REVIEW_REQUIRED",
    levelId: undefined,
    chapterId: String(lesson.chapter_id)
  };
}

async function getVocabularyHierarchy(levelId: string) {
  return api.vocabularyChapters(levelCodeFromId(levelId));
}

function vocabularyFlashcard(item: Vocabulary): FlashcardItem {
  return {
    id: item.id,
    front: item.word,
    frontSubtext: item.reading,
    back: item.meaning,
    backSubtext: item.partOfSpeech,
    tag: "Từ vựng",
    example: item.exampleMeaning ? `${item.example}\n${item.exampleMeaning}` : item.example
  };
}

function grammarFlashcard(item: Lesson): FlashcardItem {
  return {
    id: item.id,
    front: item.japaneseTitle,
    frontSubtext: item.title,
    back: item.title,
    backSubtext: "Ngữ pháp",
    tag: "Ngữ pháp"
  };
}

function kanjiFlashcard(item: Kanji): FlashcardItem {
  return {
    id: item.id,
    front: item.character,
    frontSubtext: [item.onyomi, item.kunyomi].filter(Boolean).join(" / "),
    back: item.meaning,
    backSubtext: item.hanViet ? `Hán Việt: ${item.hanViet}` : undefined,
    tag: item.topicMeaning || item.topicName,
    example: item.mnemonic
  };
}

export const apiLearningService = {
  levelCodeFromId,

  async getLevelSummaries() {
    const rawLevels = await api.levels();

    const levelsWithChapters = await Promise.all(
      rawLevels.map(async (level) => {
        try {
          const hierarchy = await api.vocabularyChapters(level.code);
          return mapLevel(level, hierarchy.chapters);
        } catch {
          return mapLevel(level);
        }
      })
    );

    return levelsWithChapters;
  },

  async getLevel(levelId: string) {
    const levels = await this.getLevelSummaries();
    return levels.find((level) => level.id === levelId);
  },

  async getChaptersPage(levelId: string) {
    const [level, hierarchy] = await Promise.all([
      this.getLevel(levelId),
      getVocabularyHierarchy(levelId)
    ]);

    return {
      level,
      chapters: hierarchy.chapters.map((chapter, index) => mapChapter(levelId, chapter, index))
    };
  },

  async getTopicPage(levelId: string, chapterId: string) {
    const { level, chapters } = await this.getChaptersPage(levelId);
    const hierarchy = await getVocabularyHierarchy(levelId);
    const rawChapter = hierarchy.chapters.find((chapter) => String(chapter.id) === chapterId);
    const chapter = chapters.find((item) => item.id === chapterId);

    return {
      level,
      chapter,
      topics: rawChapter?.topics.map((topic) => mapTopic(levelId, chapterId, topic)) ?? []
    };
  },

  async getTopicContext(levelId: string, chapterId: string, topicId: string) {
    const { level, chapter, topics } = await this.getTopicPage(levelId, chapterId);
    const topic = topics.find((item) => item.id === topicId);

    return { level, chapter, topic };
  },

  async getTopicVocabulary(levelId: string, chapterId: string, topicId: string, search = "") {
    const words = await api.vocabularies({
      level: levelCodeFromId(levelId),
      chapterId: Number(chapterId),
      topicId: Number(topicId),
      search,
      limit: 250
    });

    return words.map(mapVocabulary);
  },

  async getTopicVocabularyPage(
    levelId: string,
    chapterId: string,
    topicId: string,
    options: PageRequest = {}
  ): Promise<PaginatedLearningResult<Vocabulary>> {
    const { page, pageSize, offset } = normalizePage(options);
    const result = await api.vocabulariesPage({
      level: levelCodeFromId(levelId),
      chapterId: Number(chapterId),
      topicId: Number(topicId),
      search: options.search,
      limit: pageSize,
      offset
    });

    return {
      items: result.items.map(mapVocabulary),
      total: result.total,
      page,
      pageSize
    };
  },

  async getLevelVocabularyPage(
    levelId: string,
    options: PageRequest = {}
  ): Promise<PaginatedLearningResult<Vocabulary>> {
    const { page, pageSize, offset } = normalizePage(options);
    const result = await api.vocabulariesPage({
      level: levelCodeFromId(levelId),
      search: options.search,
      limit: pageSize,
      offset
    });

    return {
      items: result.items.map(mapVocabulary),
      total: result.total,
      page,
      pageSize
    };
  },

  async getLessons(levelId: string) {
    const lessons = await api.grammarLessons({
      level: levelCodeFromId(levelId),
      limit: 250
    });

    return lessons.map(mapGrammarLesson);
  },

  async getLessonsPage(
    levelId: string,
    options: PageRequest & { chapterId?: string } = {}
  ): Promise<PaginatedLearningResult<Lesson>> {
    const { page, pageSize, offset } = normalizePage(options);
    const result = await api.grammarLessonsPage({
      level: levelCodeFromId(levelId),
      chapterId: options.chapterId ? Number(options.chapterId) : undefined,
      search: options.search,
      limit: pageSize,
      offset
    });

    return {
      items: result.items.map((lesson) => ({
        ...mapGrammarLesson(lesson),
        levelId
      })),
      total: result.total,
      page,
      pageSize
    };
  },

  async getKanjiTopics(levelId: string) {
    const topics = await api.kanjiTopics(levelCodeFromId(levelId));
    return topics.map(mapKanjiTopic);
  },

  async getKanjiPage(
    levelId: string,
    options: PageRequest & { topicId?: string } = {}
  ): Promise<PaginatedLearningResult<Kanji>> {
    const { page, pageSize, offset } = normalizePage(options);
    const result = await api.kanjiCharactersPage({
      level: levelCodeFromId(levelId),
      topicId: options.topicId && options.topicId !== "ALL" ? Number(options.topicId) : undefined,
      search: options.search,
      limit: pageSize,
      offset
    });

    return {
      items: result.items.map(mapKanji),
      total: result.total,
      page,
      pageSize
    };
  },

  async getVocabularyFlashcards(levelId: string, chapterId?: string, topicId?: string) {
    const items = await collectAllPages((page) =>
      chapterId && topicId
        ? this.getTopicVocabularyPage(levelId, chapterId, topicId, { page, pageSize: 500 })
        : this.getLevelVocabularyPage(levelId, { page, pageSize: 500 })
    );

    return items.map(vocabularyFlashcard);
  },

  async getGrammarFlashcards(levelId: string) {
    const items = await collectAllPages((page) => this.getLessonsPage(levelId, { page, pageSize: 500 }));
    return items.map(grammarFlashcard);
  },

  async getKanjiFlashcards(levelId: string, topicId?: string) {
    const items = await collectAllPages((page) => this.getKanjiPage(levelId, { page, pageSize: 500, topicId }));
    return items.map(kanjiFlashcard);
  },

  async getLessonDetail(lessonId: string) {
    const detail = await api.grammarDetail(Number(lessonId));

    return {
      lesson: mapGrammarDetail(detail),
      detail
    };
  }
};

function mapGrammarDetail(detail: GrammarDetail): Lesson {
  return {
    id: String(detail.id),
    topicId: String(detail.chapter_id),
    lessonNumber: detail.id,
    title: detail.title || detail.pattern,
    japaneseTitle: detail.pattern,
    type: "GRAMMAR",
    durationMinutes: 8,
    vocabularyCount: detail.examples?.length ?? 0,
    patternCount: 1,
    progress: 0,
    status: "REVIEW_REQUIRED",
    chapterId: String(detail.chapter_id)
  };
}
