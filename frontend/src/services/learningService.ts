import { chapters, lessons, levels, topics, vocabularies } from "../mocks/learningData";

export const learningService = {
  getLevels: () => levels,
  getLevel: (levelId: string) => levels.find((level) => level.id === levelId),
  getChapters: (levelId: string) => chapters.filter((chapter) => chapter.levelId === levelId),
  getChapter: (chapterId: string) => chapters.find((chapter) => chapter.id === chapterId),
  getTopics: (chapterId: string) => topics.filter((topic) => topic.chapterId === chapterId),
  getTopic: (topicId: string) => topics.find((topic) => topic.id === topicId),
  getTopicVocabulary: (topicId: string) =>
    vocabularies.filter((vocabulary) => vocabulary.topicId === topicId),
  getTopicLessons: (topicId: string) => lessons.filter((lesson) => lesson.topicId === topicId),
  getLesson: (lessonId: string) => lessons.find((lesson) => lesson.id === lessonId),
  getContinueLesson: () => lessons.find((lesson) => lesson.status === "IN_PROGRESS"),
  search: (keyword: string) => {
    const normalized = keyword.trim().toLowerCase();

    if (!normalized) return [];

    return [
      ...vocabularies.filter((item) =>
        [item.word, item.reading, item.romaji, item.meaning].some((value) =>
          value.toLowerCase().includes(normalized)
        )
      ),
      ...lessons.filter((item) =>
        [item.title, item.japaneseTitle].some((value) => value.toLowerCase().includes(normalized))
      )
    ];
  }
};
