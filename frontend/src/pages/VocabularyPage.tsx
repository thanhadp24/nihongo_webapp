import { useMemo, useState } from "react";
import { Link, Navigate, useParams } from "react-router";
import { Breadcrumb } from "../components/common/Breadcrumb";
import { EmptyState } from "../components/common/StateViews";
import { FilterChips } from "../components/common/FilterChips";
import { PageHeader } from "../components/common/PageHeader";
import { SearchInput } from "../components/common/SearchInput";
import { VocabularyCard } from "../components/vocabulary/VocabularyCard";
import { learningService } from "../services/learningService";

const filters = [
  { label: "Tất cả", value: "ALL" },
  { label: "Đã học", value: "COMPLETED" },
  { label: "Cần ôn tập", value: "REVIEW_REQUIRED" },
  { label: "Đã lưu", value: "SAVED" }
];

export function VocabularyPage() {
  const { chapterId = "", levelId = "", topicId = "" } = useParams();
  const [query, setQuery] = useState("");
  const [filter, setFilter] = useState("ALL");
  const level = learningService.getLevel(levelId);
  const chapter = learningService.getChapter(chapterId);
  const topic = learningService.getTopic(topicId);
  const words = learningService.getTopicVocabulary(topicId);

  const visibleWords = useMemo(() => {
    const normalized = query.trim().toLowerCase();
    return words.filter((word) => {
      const matchesQuery =
        !normalized ||
        [word.word, word.reading, word.romaji, word.meaning].some((value) =>
          value.toLowerCase().includes(normalized)
        );
      const matchesFilter =
        filter === "ALL" ||
        (filter === "SAVED" ? word.saved : word.status === filter);
      return matchesQuery && matchesFilter;
    });
  }, [filter, query, words]);

  if (!level || !chapter || !topic) return <Navigate to="/jlpt" replace />;

  return (
    <div className="page-stack">
      <Breadcrumb
        items={[
          { label: "Trang chủ", to: "/" },
          { label: level.name, to: `/jlpt/${level.id}` },
          { label: topic.title, to: `/jlpt/${level.id}/chapters/${chapter.id}/topics/${topic.id}` },
          { label: "Từ vựng" }
        ]}
      />
      <PageHeader
        actions={
          <>
            <button className="secondary-button" type="button">Ôn tập</button>
            <button className="primary-button" type="button">Học bằng Flashcard</button>
          </>
        }
        eyebrow={topic.title}
        subtitle="Tìm kiếm, lưu từ và đánh dấu tiến độ học trong từng chủ đề."
        title="Danh sách từ vựng"
      />
      <section className="toolbar">
        <SearchInput
          onChange={setQuery}
          placeholder="Tìm từ vựng, cách đọc, romaji hoặc nghĩa..."
          value={query}
        />
        <FilterChips active={filter} items={filters} onChange={setFilter} />
      </section>
      {visibleWords.length > 0 ? (
        <section className="vocabulary-grid-cards">
          {visibleWords.map((word) => (
            <VocabularyCard item={word} key={word.id} />
          ))}
        </section>
      ) : (
        <EmptyState
          actionLabel="Xóa bộ lọc"
          onAction={() => {
            setFilter("ALL");
            setQuery("");
          }}
          text="Hãy thử từ khóa khác hoặc xóa bộ lọc."
          title="Không tìm thấy nội dung phù hợp."
        />
      )}
    </div>
  );
}
