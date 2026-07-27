export type LearningStatus =
  | "NOT_STARTED"
  | "IN_PROGRESS"
  | "COMPLETED"
  | "REVIEW_REQUIRED"
  | "LOCKED";

export type LevelTone = "n5" | "n4" | "n3" | "n2" | "n1";

export type JLPTLevel = {
  id: string;
  code: string;
  name: string;
  subtitle: string;
  description: string;
  chapterCount: number;
  topicCount: number;
  vocabularyCount: number;
  lessonCount: number;
  progress: number;
  completedChapters: number;
  status: LearningStatus;
  tone: LevelTone;
};

export type Chapter = {
  id: string;
  levelId: string;
  chapterNumber: number;
  title: string;
  description: string;
  topicCount: number;
  vocabularyCount: number;
  lessonCount: number;
  progress: number;
  status: LearningStatus;
};

export type Topic = {
  id: string;
  levelId: string;
  chapterId: string;
  topicNumber: number;
  title: string;
  japaneseTitle: string;
  description: string;
  vocabularyCount: number;
  lessonCount: number;
  exerciseCount: number;
  progress: number;
  status: LearningStatus;
  illustration: string;
};

export type Vocabulary = {
  id: string;
  topicId: string;
  word: string;
  reading: string;
  romaji: string;
  meaning: string;
  partOfSpeech: string;
  example: string;
  exampleMeaning: string;
  status: LearningStatus;
  saved: boolean;
};

export type Lesson = {
  id: string;
  topicId: string;
  lessonNumber: number;
  title: string;
  japaneseTitle: string;
  type: "VOCABULARY" | "GRAMMAR" | "KANJI" | "DIALOGUE" | "LISTENING" | "READING" | "TEST";
  durationMinutes: number;
  vocabularyCount: number;
  patternCount: number;
  progress: number;
  status: LearningStatus;
};
