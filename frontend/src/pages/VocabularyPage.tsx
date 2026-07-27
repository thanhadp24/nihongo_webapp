import { useEffect, useMemo, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { CreditCard } from "lucide-react";
import { Link, Navigate, useParams } from "react-router";
import { Breadcrumb } from "../components/common/Breadcrumb";
import { EmptyState, ErrorState, SkeletonCard } from "../components/common/StateViews";
import { FilterChips } from "../components/common/FilterChips";
import { PageHeader } from "../components/common/PageHeader";
import { Pagination } from "../components/common/Pagination";
import { SearchInput } from "../components/common/SearchInput";
import { VocabularyCard } from "../components/vocabulary/VocabularyCard";
import { apiLearningService } from "../services/apiLearningService";

const pageSize = 24;

const filters = [
  { label: "Tất cả", value: "ALL" },
  { label: "Cần ôn tập", value: "REVIEW_REQUIRED" },
  { label: "Đã lưu", value: "SAVED" }
];

export function VocabularyPage() {
  const { chapterId = "", levelId = "", topicId = "" } = useParams();
  const [query, setQuery] = useState("");
  const [filter, setFilter] = useState("ALL");
  const [page, setPage] = useState(1);

  useEffect(() => {
    setPage(1);
  }, [levelId, chapterId, topicId, query, filter]);

  const pageQuery = useQuery({
    queryKey: ["learning-vocabulary-page", levelId, chapterId, topicId],
    queryFn: () => apiLearningService.getTopicContext(levelId, chapterId, topicId),
    enabled: Boolean(levelId && chapterId && topicId)
  });
  const wordsQuery = useQuery({
    queryKey: ["learning-vocabulary", levelId, chapterId, topicId, query, page],
    queryFn: () =>
      apiLearningService.getTopicVocabularyPage(levelId, chapterId, topicId, {
        page,
        pageSize,
        search: query
      }),
    enabled: Boolean(levelId && chapterId && topicId)
  });

  const level = pageQuery.data?.level;
  const chapter = pageQuery.data?.chapter;
  const topic = pageQuery.data?.topic;
  const words = wordsQuery.data?.items ?? [];
  const total = wordsQuery.data?.total ?? 0;

  const visibleWords = useMemo(() => {
    return words.filter((word) => {
      if (filter === "ALL") return true;
      if (filter === "SAVED") return word.saved;
      return word.status === filter;
    });
  }, [filter, words]);

  if (pageQuery.data && (!level || !chapter || !topic)) return <Navigate to="/jlpt" replace />;

  return (
    <div className="page-stack">
      <Breadcrumb
        items={[
          { label: "Trang chủ", to: "/" },
          { label: level?.name ?? levelId.toUpperCase(), to: `/jlpt/${levelId}` },
          {
            label: topic?.title ?? "Chủ đề",
            to: `/jlpt/${levelId}/chapters/${chapterId}/topics/${topicId}`
          },
          { label: "Từ vựng" }
        ]}
      />
      <PageHeader
        actions={
          <>
            <Link className="secondary-button" to={`/jlpt/${levelId}/vocabulary`}>
              Xem cả level
            </Link>
            <Link
              className="primary-button"
              to={`/jlpt/${levelId}/chapters/${chapterId}/topics/${topicId}/vocabulary/flashcards`}
            >
              <CreditCard aria-hidden="true" />
              Học bằng Flashcard
            </Link>
          </>
        }
        eyebrow={topic?.title ?? "Chủ đề"}
        subtitle="Từ vựng được lấy trực tiếp từ CSDL theo level, chapter và topic."
        title="Danh sách từ vựng"
      />
      <section className="toolbar">
        <SearchInput
          onChange={setQuery}
          placeholder="Tìm từ vựng, cách đọc hoặc nghĩa..."
          value={query}
        />
        <FilterChips active={filter} items={filters} onChange={setFilter} />
      </section>
      {pageQuery.isLoading || wordsQuery.isLoading ? <SkeletonCard count={6} /> : null}
      {pageQuery.isError || wordsQuery.isError ? (
        <ErrorState
          onRetry={() => {
            pageQuery.refetch();
            wordsQuery.refetch();
          }}
        />
      ) : null}
      {visibleWords.length > 0 ? (
        <>
          <section className="vocabulary-grid-cards">
            {visibleWords.map((word) => (
              <VocabularyCard item={word} key={word.id} />
            ))}
          </section>
          <Pagination onPageChange={setPage} page={page} pageSize={pageSize} total={total} />
        </>
      ) : (
        !wordsQuery.isLoading && (
          <EmptyState
            actionLabel="Xóa bộ lọc"
            onAction={() => {
              setFilter("ALL");
              setQuery("");
            }}
            text="Hãy thử từ khóa khác hoặc xóa bộ lọc."
            title="Không tìm thấy nội dung phù hợp."
          />
        )
      )}
    </div>
  );
}
