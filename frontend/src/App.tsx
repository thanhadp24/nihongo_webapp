import { useEffect, useState } from "react";
import { NavLink, Navigate, Route, Routes } from "react-router";
import { useQuery } from "@tanstack/react-query";
import { api } from "./api";
import type {
  GrammarChapter,
  GrammarDetail,
  GrammarLesson,
  KanjiCharacter,
  KanjiDetail,
  KanjiTopic,
  VocabularyChapter,
  VocabularyItem
} from "./types";

const fallbackLevels = ["N5", "N4", "N3", "N2", "N1"];

const modules = [
  { path: "/vocabulary", label: "Từ vựng", key: "vocabulary_count" },
  { path: "/kanji", label: "Kanji", key: "kanji_count" },
  { path: "/grammar", label: "Ngữ pháp", key: "grammar_count" }
] as const;

// Custom React Hook to detect mobile screens
function useIsMobile() {
  const [isMobile, setIsMobile] = useState(window.innerWidth < 768);
  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth < 768);
    };
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);
  return isMobile;
}

function App() {
  const [level, setLevel] = useState("N5");
  const levelsQuery = useQuery({
    queryKey: ["jlpt-levels"],
    queryFn: api.levels
  });

  const levels = levelsQuery.data ?? [];
  const levelCodes = levels.length > 0 ? levels.map((item) => item.code) : fallbackLevels;
  const activeLevel = levels.find((item) => item.code === level);

  useEffect(() => {
    if (levels.length > 0 && !levels.some((item) => item.code === level)) {
      setLevel(levels[0].code);
    }
  }, [level, levels]);

  return (
    <main className="app-shell">
      <header className="topbar">
        <div className="brand">
          <span className="brand-mark">日</span>
          <div>
            <p className="eyebrow">Nihongo Webapp</p>
            <h1>JLPT Study Desk</h1>
          </div>
        </div>

        <div className="level-switcher" aria-label="Chọn cấp độ JLPT">
          {levelCodes.map((code) => (
            <button
              className={code === level ? "level-chip active" : "level-chip"}
              key={code}
              onClick={() => setLevel(code)}
              type="button"
            >
              {code}
            </button>
          ))}
        </div>
      </header>

      <nav className="module-tabs" aria-label="Tính năng học">
        {modules.map((module) => (
          <NavLink className="module-tab" key={module.path} to={module.path}>
            <span>{module.label}</span>
            {activeLevel ? <strong>{activeLevel[module.key]}</strong> : null}
          </NavLink>
        ))}
      </nav>

      <Routes>
        <Route element={<Navigate to="/vocabulary" replace />} path="/" />
        <Route element={<VocabularyPage level={level} />} path="/vocabulary" />
        <Route element={<KanjiPage level={level} />} path="/kanji" />
        <Route element={<GrammarPage level={level} />} path="/grammar" />
      </Routes>
    </main>
  );
}

function VocabularyPage({ level }: { level: string }) {
  const isMobile = useIsMobile();
  const [mobileView, setMobileView] = useState<'list' | 'detail'>('list');
  const [isFilterOpen, setIsFilterOpen] = useState(false);

  const [chapterId, setChapterId] = useState<number | null>(null);
  const [topicId, setTopicId] = useState<number | null>(null);
  const [search, setSearch] = useState("");
  const [selectedWordId, setSelectedWordId] = useState<number | null>(null);

  useEffect(() => {
    setChapterId(null);
    setTopicId(null);
    setSearch("");
    setSelectedWordId(null);
    setMobileView('list');
    setIsFilterOpen(false);
  }, [level]);

  const chaptersQuery = useQuery({
    queryKey: ["vocabulary-chapters", level],
    queryFn: () => api.vocabularyChapters(level)
  });

  const wordsQuery = useQuery({
    queryKey: ["vocabularies", level, chapterId, topicId, search],
    queryFn: () => api.vocabularies({ level, chapterId, topicId, search })
  });

  const words = wordsQuery.data ?? [];
  const selectedWord = words.find((word) => word.id === selectedWordId) ?? words[0];

  useEffect(() => {
    if (words.length > 0 && !words.some((word) => word.id === selectedWordId)) {
      setSelectedWordId(words[0].id);
    }
  }, [selectedWordId, words]);

  return (
    <FeatureFrame
      isMobile={isMobile}
      isFilterOpen={isFilterOpen}
      setIsFilterOpen={setIsFilterOpen}
      aside={
        <VocabularyFilters
          chapterId={chapterId}
          chapters={chaptersQuery.data?.chapters ?? []}
          isLoading={chaptersQuery.isLoading}
          onChapterChange={(id) => {
            setChapterId(id);
            setTopicId(null);
            setIsFilterOpen(false);
            setMobileView('list');
          }}
          onTopicChange={(id) => {
            setTopicId(id);
            setIsFilterOpen(false);
            setMobileView('list');
          }}
          topicId={topicId}
        />
      }
      eyebrow={`${level} vocabulary`}
      search={search}
      searchPlaceholder="Tìm từ, cách đọc, nghĩa..."
      title="Từ vựng"
      total={words.length}
      onSearchChange={(val) => {
        setSearch(val);
        setMobileView('list');
      }}
    >
      <QueryBoundary isError={wordsQuery.isError} isLoading={wordsQuery.isLoading}>
        {words.length === 0 ? (
          <EmptyState text="Chưa có từ vựng phù hợp với bộ lọc hiện tại." />
        ) : (
          <div className={`study-grid vocabulary-grid ${isMobile ? `mobile-${mobileView}` : ''}`}>
            {(!isMobile || mobileView === 'list') && (
              <div className="list-pane">
                {words.map((word) => (
                  <button
                    className={selectedWord?.id === word.id ? "word-row active" : "word-row"}
                    key={word.id}
                    onClick={() => {
                      setSelectedWordId(word.id);
                      if (isMobile) setMobileView('detail');
                    }}
                    type="button"
                  >
                    <span>
                      <strong>{word.word}</strong>
                      <small>{word.reading || word.topic_name}</small>
                    </span>
                    <em>{word.meaning_vi}</em>
                  </button>
                ))}
              </div>
            )}
            {(!isMobile || mobileView === 'detail') && (
              <VocabularyDetail 
                word={selectedWord} 
                isMobile={isMobile}
                onBack={() => setMobileView('list')}
              />
            )}
          </div>
        )}
      </QueryBoundary>
    </FeatureFrame>
  );
}

function VocabularyFilters({
  chapterId,
  chapters,
  isLoading,
  onChapterChange,
  onTopicChange,
  topicId
}: {
  chapterId: number | null;
  chapters: VocabularyChapter[];
  isLoading: boolean;
  onChapterChange: (id: number | null) => void;
  onTopicChange: (id: number | null) => void;
  topicId: number | null;
}) {
  return (
    <div className="filter-stack">
      <button
        className={chapterId === null && topicId === null ? "filter-button active" : "filter-button"}
        onClick={() => {
          onChapterChange(null);
          onTopicChange(null);
        }}
        type="button"
      >
        <span>Tất cả chapter</span>
      </button>
      {isLoading ? <SkeletonRows /> : null}
      {chapters.map((chapter) => (
        <section className="filter-group" key={chapter.id}>
          <button
            className={chapterId === chapter.id && topicId === null ? "filter-button active" : "filter-button"}
            onClick={() => onChapterChange(chapter.id)}
            type="button"
          >
            <span>
              Bài {chapter.chapter_number}: {chapter.name}
            </span>
            <small>{chapter.topics.reduce((total, topic) => total + topic.vocabulary_count, 0)}</small>
          </button>
          <div className="nested-filters">
            {chapter.topics.map((topic) => (
              <button
                className={topicId === topic.id ? "topic-filter active" : "topic-filter"}
                key={topic.id}
                onClick={() => {
                  onChapterChange(chapter.id);
                  onTopicChange(topic.id);
                }}
                type="button"
              >
                <span>{topic.name}</span>
                <small>{topic.vocabulary_count}</small>
              </button>
            ))}
          </div>
        </section>
      ))}
    </div>
  );
}

function VocabularyDetail({ 
  word, 
  isMobile, 
  onBack 
}: { 
  word?: VocabularyItem;
  isMobile: boolean;
  onBack: () => void;
}) {
  if (!word) {
    return <EmptyState text="Chọn một từ để xem chi tiết." />;
  }

  return (
    <article className="detail-pane">
      {isMobile && (
        <button className="back-btn" onClick={onBack} type="button">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
            <line x1="19" y1="12" x2="5" y2="12"></line>
            <polyline points="12 19 5 12 12 5"></polyline>
          </svg>
          Quay lại danh sách
        </button>
      )}
      <p className="eyebrow">{word.chapter_name} / {word.topic_name}</p>
      <h2 className="japanese-title">{word.word}</h2>
      <p className="reading-line">{word.reading || "Không có cách đọc"}</p>
      <div className="meaning-box">{word.meaning_vi}</div>
      <InfoGrid
        items={[
          ["Loại từ", word.part_of_speech || "Chưa phân loại"],
          ["Topic", word.topic_name]
        ]}
      />
      <ExampleBlock
        meaning={word.example_meaning_vi}
        reading={word.example_reading}
        text={word.example_sentence}
      />
    </article>
  );
}

function KanjiPage({ level }: { level: string }) {
  const isMobile = useIsMobile();
  const [mobileView, setMobileView] = useState<'list' | 'detail'>('list');
  const [isFilterOpen, setIsFilterOpen] = useState(false);

  const [topicId, setTopicId] = useState<number | null>(null);
  const [search, setSearch] = useState("");
  const [selectedId, setSelectedId] = useState<number | null>(null);

  useEffect(() => {
    setTopicId(null);
    setSearch("");
    setSelectedId(null);
    setMobileView('list');
    setIsFilterOpen(false);
  }, [level]);

  const topicsQuery = useQuery({
    queryKey: ["kanji-topics", level],
    queryFn: () => api.kanjiTopics(level)
  });
  const charactersQuery = useQuery({
    queryKey: ["kanji-characters", level, topicId, search],
    queryFn: () => api.kanjiCharacters({ level, topicId, search })
  });

  const characters = charactersQuery.data ?? [];
  const selectedListItem = characters.find((item) => item.id === selectedId) ?? characters[0];
  const detailQuery = useQuery({
    queryKey: ["kanji-detail", selectedListItem?.id],
    queryFn: () => api.kanjiDetail(selectedListItem!.id),
    enabled: Boolean(selectedListItem)
  });

  useEffect(() => {
    if (characters.length > 0 && !characters.some((item) => item.id === selectedId)) {
      setSelectedId(characters[0].id);
    }
  }, [characters, selectedId]);

  return (
    <FeatureFrame
      isMobile={isMobile}
      isFilterOpen={isFilterOpen}
      setIsFilterOpen={setIsFilterOpen}
      aside={
        <TopicFilters
          activeId={topicId}
          allLabel="Tất cả chủ đề"
          countKey="character_count"
          isLoading={topicsQuery.isLoading}
          items={topicsQuery.data ?? []}
          labelKey="name_vi"
          onChange={(id) => {
            setTopicId(id);
            setIsFilterOpen(false);
            setMobileView('list');
          }}
        />
      }
      eyebrow={`${level} kanji`}
      search={search}
      searchPlaceholder="Tìm kanji, âm đọc, nghĩa..."
      title="Kanji"
      total={characters.length}
      onSearchChange={(val) => {
        setSearch(val);
        setMobileView('list');
      }}
    >
      <QueryBoundary isError={charactersQuery.isError} isLoading={charactersQuery.isLoading}>
        {characters.length === 0 ? (
          <EmptyState text="Chưa có kanji phù hợp với bộ lọc hiện tại." />
        ) : (
          <div className={`study-grid kanji-layout ${isMobile ? `mobile-${mobileView}` : ''}`}>
            {(!isMobile || mobileView === 'list') && (
              <div className="kanji-board">
                {characters.map((character) => (
                  <button
                    className={selectedListItem?.id === character.id ? "kanji-tile active" : "kanji-tile"}
                    key={character.id}
                    onClick={() => {
                      setSelectedId(character.id);
                      if (isMobile) setMobileView('detail');
                    }}
                    type="button"
                  >
                    <strong>{character.character_value}</strong>
                    <span>{character.meaning_vi}</span>
                  </button>
                ))}
              </div>
            )}
            {(!isMobile || mobileView === 'detail') && (
              <KanjiDetailPanel
                detail={detailQuery.data}
                fallback={selectedListItem}
                isLoading={detailQuery.isLoading}
                isMobile={isMobile}
                onBack={() => setMobileView('list')}
              />
            )}
          </div>
        )}
      </QueryBoundary>
    </FeatureFrame>
  );
}

function KanjiDetailPanel({
  detail,
  fallback,
  isLoading,
  isMobile,
  onBack
}: {
  detail?: KanjiDetail;
  fallback?: KanjiCharacter;
  isLoading: boolean;
  isMobile: boolean;
  onBack: () => void;
}) {
  const kanji = detail ?? fallback;

  if (!kanji) {
    return <EmptyState text="Chọn một kanji để xem chi tiết." />;
  }

  return (
    <article className="detail-pane">
      {isMobile && (
        <button className="back-btn" onClick={onBack} type="button">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
            <line x1="19" y1="12" x2="5" y2="12"></line>
            <polyline points="12 19 5 12 12 5"></polyline>
          </svg>
          Quay lại danh sách
        </button>
      )}
      <p className="eyebrow">{kanji.topic_name_vi || kanji.topic_name}</p>
      <h2 className="kanji-title">{kanji.character_value}</h2>
      <div className="meaning-box">{kanji.meaning_vi}</div>
      <InfoGrid
        items={[
          ["Hán Việt", kanji.han_viet || "Chưa có"],
          ["Onyomi", kanji.onyomi || "Chưa có"],
          ["Kunyomi", kanji.kunyomi || "Chưa có"],
          ["Số nét", kanji.stroke_count ? String(kanji.stroke_count) : "Chưa có"]
        ]}
      />
      {kanji.mnemonic_vi ? <p className="note-box">{kanji.mnemonic_vi}</p> : null}
      {isLoading ? <SkeletonRows /> : null}
      {detail?.words?.length ? (
        <div className="word-examples">
          <h3>Từ liên quan</h3>
          {detail.words.map((word) => (
            <ExampleBlock
              key={word.id}
              label={`${word.word}${word.reading ? ` - ${word.reading}` : ""}`}
              meaning={word.example_meaning_vi || word.meaning_vi}
              reading={word.example_reading}
              text={word.example_sentence}
            />
          ))}
        </div>
      ) : null}
    </article>
  );
}

function GrammarPage({ level }: { level: string }) {
  const isMobile = useIsMobile();
  const [mobileView, setMobileView] = useState<'list' | 'detail'>('list');
  const [isFilterOpen, setIsFilterOpen] = useState(false);

  const [chapterId, setChapterId] = useState<number | null>(null);
  const [search, setSearch] = useState("");
  const [selectedId, setSelectedId] = useState<number | null>(null);

  useEffect(() => {
    setChapterId(null);
    setSearch("");
    setSelectedId(null);
    setMobileView('list');
    setIsFilterOpen(false);
  }, [level]);

  const chaptersQuery = useQuery({
    queryKey: ["grammar-chapters", level],
    queryFn: () => api.grammarChapters(level)
  });
  const lessonsQuery = useQuery({
    queryKey: ["grammar-lessons", level, chapterId, search],
    queryFn: () => api.grammarLessons({ level, chapterId, search })
  });

  const lessons = lessonsQuery.data ?? [];
  const selectedListItem = lessons.find((lesson) => lesson.id === selectedId) ?? lessons[0];
  const detailQuery = useQuery({
    queryKey: ["grammar-detail", selectedListItem?.id],
    queryFn: () => api.grammarDetail(selectedListItem!.id),
    enabled: Boolean(selectedListItem)
  });

  useEffect(() => {
    if (lessons.length > 0 && !lessons.some((lesson) => lesson.id === selectedId)) {
      setSelectedId(lessons[0].id);
    }
  }, [lessons, selectedId]);

  return (
    <FeatureFrame
      isMobile={isMobile}
      isFilterOpen={isFilterOpen}
      setIsFilterOpen={setIsFilterOpen}
      aside={
        <TopicFilters
          activeId={chapterId}
          allLabel="Tất cả bài"
          countKey="lesson_count"
          isLoading={chaptersQuery.isLoading}
          items={chaptersQuery.data ?? []}
          labelKey="name"
          onChange={(id) => {
            setChapterId(id);
            setIsFilterOpen(false);
            setMobileView('list');
          }}
        />
      }
      eyebrow={`${level} grammar`}
      search={search}
      searchPlaceholder="Tìm mẫu câu, nghĩa, giải thích..."
      title="Ngữ pháp"
      total={lessons.length}
      onSearchChange={(val) => {
        setSearch(val);
        setMobileView('list');
      }}
    >
      <QueryBoundary isError={lessonsQuery.isError} isLoading={lessonsQuery.isLoading}>
        {lessons.length === 0 ? (
          <EmptyState text="Chưa có ngữ pháp phù hợp với bộ lọc hiện tại." />
        ) : (
          <div className={`study-grid grammar-layout ${isMobile ? `mobile-${mobileView}` : ''}`}>
            {(!isMobile || mobileView === 'list') && (
              <div className="list-pane">
                {lessons.map((lesson) => (
                  <button
                    className={selectedListItem?.id === lesson.id ? "lesson-row active" : "lesson-row"}
                    key={lesson.id}
                    onClick={() => {
                      setSelectedId(lesson.id);
                      if (isMobile) setMobileView('detail');
                    }}
                    type="button"
                  >
                    <strong>{lesson.pattern}</strong>
                    <span>{lesson.title}</span>
                    <small>Bài {lesson.chapter_number}</small>
                  </button>
                ))}
              </div>
            )}
            {(!isMobile || mobileView === 'detail') && (
              <GrammarDetailPanel
                detail={detailQuery.data}
                fallback={selectedListItem}
                isLoading={detailQuery.isLoading}
                isMobile={isMobile}
                onBack={() => setMobileView('list')}
              />
            )}
          </div>
        )}
      </QueryBoundary>
    </FeatureFrame>
  );
}

function GrammarDetailPanel({
  detail,
  fallback,
  isLoading,
  isMobile,
  onBack
}: {
  detail?: GrammarDetail;
  fallback?: GrammarLesson;
  isLoading: boolean;
  isMobile: boolean;
  onBack: () => void;
}) {
  const lesson = detail ?? fallback;

  if (!lesson) {
    return <EmptyState text="Chọn một mẫu ngữ pháp để xem chi tiết." />;
  }

  return (
    <article className="detail-pane">
      {isMobile && (
        <button className="back-btn" onClick={onBack} type="button">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
            <line x1="19" y1="12" x2="5" y2="12"></line>
            <polyline points="12 19 5 12 12 5"></polyline>
          </svg>
          Quay lại danh sách
        </button>
      )}
      <p className="eyebrow">{lesson.chapter_name}</p>
      <h2 className="pattern-title">{lesson.pattern}</h2>
      <div className="meaning-box">{lesson.meaning_vi || lesson.title}</div>
      {lesson.formation ? (
        <section className="text-section">
          <h3>Cấu trúc</h3>
          <p>{lesson.formation}</p>
        </section>
      ) : null}
      {lesson.explanation ? (
        <section className="text-section">
          <h3>Giải thích</h3>
          <p>{lesson.explanation}</p>
        </section>
      ) : null}
      {isLoading ? <SkeletonRows /> : null}
      {detail?.examples?.length ? (
        <div className="word-examples">
          <h3>Ví dụ</h3>
          {detail.examples.map((example) => (
            <ExampleBlock
              key={example.id}
              meaning={example.meaning_vi}
              reading={example.reading}
              text={example.japanese_text}
            />
          ))}
        </div>
      ) : null}
    </article>
  );
}

function FeatureFrame({
  aside,
  children,
  eyebrow,
  search,
  searchPlaceholder,
  title,
  total,
  onSearchChange,
  isMobile,
  isFilterOpen,
  setIsFilterOpen
}: {
  aside: React.ReactNode;
  children: React.ReactNode;
  eyebrow: string;
  search: string;
  searchPlaceholder: string;
  title: string;
  total: number;
  onSearchChange: (value: string) => void;
  isMobile: boolean;
  isFilterOpen: boolean;
  setIsFilterOpen: (open: boolean) => void;
}) {
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);

  return (
    <section className={`feature-shell ${isSidebarCollapsed && !isMobile ? "sidebar-collapsed" : ""}`}>
      {/* Mobile Drawer */}
      {isMobile && isFilterOpen && (
        <div className="drawer-overlay" onClick={() => setIsFilterOpen(false)}>
          <div className="drawer-content" onClick={(e) => e.stopPropagation()}>
            <div className="drawer-header">
              <h3>Bộ lọc bài học</h3>
              <button className="drawer-close" onClick={() => setIsFilterOpen(false)} type="button">
                ✕
              </button>
            </div>
            <div className="drawer-body">{aside}</div>
          </div>
        </div>
      )}

      {/* Desktop Sidebar */}
      {!isMobile && (
        <aside className="filter-panel">
          <div className="sidebar-header">
            <h3>Bộ lọc bài học</h3>
            <button
              className="sidebar-toggle-btn"
              onClick={() => setIsSidebarCollapsed(true)}
              title="Thu gọn bộ lọc"
              type="button"
            >
              ←
            </button>
          </div>
          {aside}
        </aside>
      )}

      {/* Main Content Area */}
      <section className="content-panel">
        <header className="content-header">
          <div className="content-header-title">
            {!isMobile && isSidebarCollapsed && (
              <button
                className="sidebar-expand-btn"
                onClick={() => setIsSidebarCollapsed(false)}
                title="Mở bộ lọc"
                type="button"
              >
                →
              </button>
            )}
            <div>
              <p className="eyebrow">{eyebrow}</p>
              <h2>{title}</h2>
            </div>
          </div>
          <div className="header-tools">
            {isMobile && (
              <button
                className="mobile-filter-trigger"
                onClick={() => setIsFilterOpen(true)}
                type="button"
              >
                <svg
                  width="18"
                  height="18"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2.5"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <line x1="4" y1="21" x2="4" y2="14"></line>
                  <line x1="4" y1="10" x2="4" y2="3"></line>
                  <line x1="12" y1="21" x2="12" y2="12"></line>
                  <line x1="12" y1="8" x2="12" y2="3"></line>
                  <line x1="20" y1="21" x2="20" y2="16"></line>
                  <line x1="20" y1="12" x2="20" y2="3"></line>
                  <line x1="1" y1="14" x2="7" y2="14"></line>
                  <line x1="9" y1="8" x2="15" y2="8"></line>
                  <line x1="17" y1="16" x2="23" y2="16"></line>
                </svg>
                Bộ lọc
              </button>
            )}
            <label className="search-field">
              <span>Tìm kiếm</span>
              <div className="search-input-wrapper">
                <svg
                  className="search-icon-svg"
                  width="18"
                  height="18"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2.5"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                >
                  <circle cx="11" cy="11" r="8"></circle>
                  <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                </svg>
                <input
                  onChange={(event) => onSearchChange(event.target.value)}
                  placeholder={searchPlaceholder}
                  value={search}
                />
              </div>
            </label>
            <div className="metric-box">
              <span>Kết quả</span>
              <strong>{total}</strong>
            </div>
          </div>
        </header>
        {children}
      </section>
    </section>
  );
}

function TopicFilters<T extends KanjiTopic | GrammarChapter>({
  activeId,
  allLabel,
  countKey,
  isLoading,
  items,
  labelKey,
  onChange
}: {
  activeId: number | null;
  allLabel: string;
  countKey: keyof T;
  isLoading: boolean;
  items: T[];
  labelKey: keyof T;
  onChange: (id: number | null) => void;
}) {
  return (
    <div className="filter-stack">
      <button
        className={activeId === null ? "filter-button active" : "filter-button"}
        onClick={() => onChange(null)}
        type="button"
      >
        <span>{allLabel}</span>
      </button>
      {isLoading ? <SkeletonRows /> : null}
      {items.map((item) => {
        const label = item[labelKey] || "Chưa đặt tên";
        const count = item[countKey];

        return (
          <button
            className={activeId === item.id ? "filter-button active" : "filter-button"}
            key={item.id}
            onClick={() => onChange(item.id)}
            type="button"
          >
            <span>{String(label)}</span>
            <small>{String(count)}</small>
          </button>
        );
      })}
    </div>
  );
}

function QueryBoundary({
  children,
  isError,
  isLoading
}: {
  children: React.ReactNode;
  isError: boolean;
  isLoading: boolean;
}) {
  if (isLoading) {
    return (
      <div className="state-card">
        <span className="loader" />
        <strong>Đang tải dữ liệu...</strong>
      </div>
    );
  }

  if (isError) {
    return <EmptyState text="Không tải được dữ liệu từ API. Kiểm tra backend và kết nối MySQL." />;
  }

  return <>{children}</>;
}

function EmptyState({ text }: { text: string }) {
  return (
    <div className="state-card">
      <strong>{text}</strong>
    </div>
  );
}

function SkeletonRows() {
  return (
    <div className="skeleton-stack" aria-hidden="true">
      <span />
      <span />
      <span />
    </div>
  );
}

function InfoGrid({ items }: { items: [string, string][] }) {
  return (
    <dl className="info-grid">
      {items.map(([label, value]) => (
        <div key={label}>
          <dt>{label}</dt>
          <dd>{value}</dd>
        </div>
      ))}
    </dl>
  );
}

function ExampleBlock({
  label,
  meaning,
  reading,
  text
}: {
  label?: string;
  meaning: string | null;
  reading: string | null;
  text: string | null;
}) {
  if (!label && !meaning && !reading && !text) {
    return null;
  }

  return (
    <section className="example-block">
      {label ? <strong>{label}</strong> : null}
      {text ? <p className="example-jp">{text}</p> : null}
      {reading ? <p className="example-reading">{reading}</p> : null}
      {meaning ? <p>{meaning}</p> : null}
    </section>
  );
}

export default App;
