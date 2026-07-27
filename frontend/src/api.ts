import type {
  GrammarChapter,
  GrammarDetail,
  GrammarLesson,
  JlptLevel,
  KanjiCharacter,
  KanjiDetail,
  KanjiTopic,
  VocabularyHierarchy,
  VocabularyItem
} from "./types";

const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api"
).replace(/\/$/, "");

type QueryValue = string | number | null | undefined;

export type PaginatedResult<T> = {
  items: T[];
  total: number;
};

function buildPath(path: string, params: Record<string, QueryValue> = {}) {
  const url = new URL(`${API_BASE_URL}${path}`);

  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== "") {
      url.searchParams.set(key, String(value));
    }
  });

  return url.toString();
}

async function request<T>(path: string, params?: Record<string, QueryValue>): Promise<T> {
  const response = await fetch(buildPath(path, params));

  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || `Request failed with ${response.status}`);
  }

  return response.json() as Promise<T>;
}

async function requestPaginated<T>(
  path: string,
  params?: Record<string, QueryValue>
): Promise<PaginatedResult<T>> {
  const response = await fetch(buildPath(path, params));

  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || `Request failed with ${response.status}`);
  }

  const total = Number(response.headers.get("X-Total-Count") ?? 0);
  const items = (await response.json()) as T[];

  return {
    items,
    total: Number.isFinite(total) ? total : items.length
  };
}

export const api = {
  levels: () => request<JlptLevel[]>("/jlpt-levels"),
  vocabularyChapters: (level: string) =>
    request<VocabularyHierarchy>("/vocabulary/chapters", { level }),
  vocabularies: (params: {
    level: string;
    chapterId?: number | null;
    topicId?: number | null;
    search?: string;
    limit?: number;
    offset?: number;
  }) =>
    request<VocabularyItem[]>("/vocabularies", {
      level: params.level,
      chapter_id: params.chapterId,
      topic_id: params.topicId,
      search: params.search,
      limit: params.limit,
      offset: params.offset
    }),
  vocabulariesPage: (params: {
    level: string;
    chapterId?: number | null;
    topicId?: number | null;
    search?: string;
    limit?: number;
    offset?: number;
  }) =>
    requestPaginated<VocabularyItem>("/vocabularies", {
      level: params.level,
      chapter_id: params.chapterId,
      topic_id: params.topicId,
      search: params.search,
      limit: params.limit,
      offset: params.offset
    }),
  kanjiTopics: (level: string) => request<KanjiTopic[]>("/kanji/topics", { level }),
  kanjiCharacters: (params: {
    level: string;
    topicId?: number | null;
    search?: string;
    limit?: number;
    offset?: number;
  }) =>
    request<KanjiCharacter[]>("/kanji/characters", {
      level: params.level,
      topic_id: params.topicId,
      search: params.search,
      limit: params.limit,
      offset: params.offset
    }),
  kanjiCharactersPage: (params: {
    level: string;
    topicId?: number | null;
    search?: string;
    limit?: number;
    offset?: number;
  }) =>
    requestPaginated<KanjiCharacter>("/kanji/characters", {
      level: params.level,
      topic_id: params.topicId,
      search: params.search,
      limit: params.limit,
      offset: params.offset
    }),
  kanjiDetail: (id: number) => request<KanjiDetail>(`/kanji/characters/${id}`),
  grammarChapters: (level: string) => request<GrammarChapter[]>("/grammar/chapters", { level }),
  grammarLessons: (params: {
    level: string;
    chapterId?: number | null;
    search?: string;
    limit?: number;
    offset?: number;
  }) =>
    request<GrammarLesson[]>("/grammar/lessons", {
      level: params.level,
      chapter_id: params.chapterId,
      search: params.search,
      limit: params.limit,
      offset: params.offset
    }),
  grammarLessonsPage: (params: {
    level: string;
    chapterId?: number | null;
    search?: string;
    limit?: number;
    offset?: number;
  }) =>
    requestPaginated<GrammarLesson>("/grammar/lessons", {
      level: params.level,
      chapter_id: params.chapterId,
      search: params.search,
      limit: params.limit,
      offset: params.offset
    }),
  grammarDetail: (id: number) => request<GrammarDetail>(`/grammar/lessons/${id}`)
};
