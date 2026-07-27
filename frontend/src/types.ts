export type JlptLevel = {
  id: number;
  code: string;
  name: string;
  description: string | null;
  display_order: number;
  vocabulary_count: number;
  kanji_count: number;
  grammar_count: number;
};

export type VocabularyTopic = {
  id: number;
  section_number: number;
  name: string;
  description: string | null;
  vocabulary_count: number;
};

export type VocabularyChapter = {
  id: number;
  chapter_number: number;
  name: string;
  reading: string | null;
  description: string | null;
  topics: VocabularyTopic[];
};

export type VocabularyHierarchy = {
  level: string;
  chapters: VocabularyChapter[];
};

export type VocabularyItem = {
  id: number;
  word: string;
  reading: string | null;
  meaning_vi: string;
  part_of_speech: string | null;
  example_sentence: string | null;
  example_reading: string | null;
  example_meaning_vi: string | null;
  topic_id: number;
  topic_name: string;
  chapter_id: number;
  chapter_name: string;
};

export type KanjiTopic = {
  id: number;
  name: string;
  name_reading: string | null;
  name_vi: string | null;
  description: string | null;
  source_book: string | null;
  source_week: number | null;
  source_day: number | null;
  display_order: number;
  character_count: number;
};

export type KanjiCharacter = {
  id: number;
  character_value: string;
  han_viet: string | null;
  onyomi: string | null;
  kunyomi: string | null;
  meaning_vi: string;
  stroke_count: number | null;
  mnemonic_vi: string | null;
  topic_id: number;
  topic_name: string;
  topic_name_vi: string | null;
};

export type KanjiWord = {
  id: number;
  word: string;
  reading: string | null;
  meaning_vi: string;
  example_sentence: string | null;
  example_reading: string | null;
  example_meaning_vi: string | null;
};

export type KanjiDetail = KanjiCharacter & {
  words: KanjiWord[];
};

export type GrammarChapter = {
  id: number;
  chapter_number: number;
  name: string;
  description: string | null;
  display_order: number;
  lesson_count: number;
};

export type GrammarLesson = {
  id: number;
  title: string;
  pattern: string;
  meaning_vi: string | null;
  explanation: string | null;
  formation: string | null;
  example_japanese?: string | null;
  example_reading?: string | null;
  example_meaning_vi?: string | null;
  chapter_id: number;
  chapter_name: string;
  chapter_number: number;
};

export type GrammarExample = {
  id: number;
  japanese_text: string;
  reading: string | null;
  meaning_vi: string | null;
};

export type GrammarDetail = GrammarLesson & {
  examples: GrammarExample[];
};
