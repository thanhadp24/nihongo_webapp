import { useEffect, useMemo, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { CreditCard } from "lucide-react";
import { Link, Navigate, useParams } from "react-router";
import { Breadcrumb } from "../components/common/Breadcrumb";
import { EmptyState, ErrorState, SkeletonCard } from "../components/common/StateViews";
import { FilterChips } from "../components/common/FilterChips";
import { LevelSelector } from "../components/common/LevelSelector";
import { PageHeader } from "../components/common/PageHeader";
import { Pagination } from "../components/common/Pagination";
import { SearchInput } from "../components/common/SearchInput";
import { KanjiCard } from "../components/kanji/KanjiCard";
import { apiLearningService } from "../services/apiLearningService";

const pageSize = 24;

export function KanjiPage() {
  const { levelId = "n2" } = useParams();
  const [query, setQuery] = useState("");
  const [topicId, setTopicId] = useState("ALL");
  const [page, setPage] = useState(1);

  useEffect(() => {
    setPage(1);
  }, [levelId, query, topicId]);

  const levelQuery = useQuery({
    queryKey: ["learning-level", levelId],
    queryFn: () => apiLearningService.getLevel(levelId),
    enabled: Boolean(levelId)
  });
  const topicsQuery = useQuery({
    queryKey: ["learning-kanji-topics", levelId],
    queryFn: () => apiLearningService.getKanjiTopics(levelId),
    enabled: Boolean(levelId)
  });
  const kanjiQuery = useQuery({
    queryKey: ["learning-kanji-page", levelId, topicId, query, page],
    queryFn: () => apiLearningService.getKanjiPage(levelId, { page, pageSize, search: query, topicId }),
    enabled: Boolean(levelId)
  });

  const level = levelQuery.data;
  const topics = topicsQuery.data ?? [];
  const kanji = kanjiQuery.data?.items ?? [];
  const total = kanjiQuery.data?.total ?? 0;
  const topicFilters = useMemo(
    () => [
      { label: "Tất cả", value: "ALL" },
      ...topics.map((topic) => ({
        label: topic.meaning || topic.title,
        value: topic.id
      }))
    ],
    [topics]
  );

  if (levelQuery.data === undefined && levelQuery.isSuccess) return <Navigate to="/jlpt" replace />;

  return (
    <div className="page-stack">
      <Breadcrumb
        items={[
          { label: "Trang chủ", to: "/" },
          { label: level?.name ?? levelId.toUpperCase(), to: `/jlpt/${levelId}` },
          { label: "Kanji" }
        ]}
      />
      <PageHeader
        actions={
          <>
            <LevelSelector value={levelId} toForLevel={(nextLevel) => `/jlpt/${nextLevel}/kanji`} />
            <Link
              className="primary-button"
              to={`/jlpt/${levelId}/kanji/flashcards${topicId === "ALL" ? "" : `?topicId=${topicId}`}`}
            >
              <CreditCard aria-hidden="true" />
              Flashcard
            </Link>
          </>
        }
        eyebrow={level?.name ?? "JLPT"}
        subtitle="Chọn level và chủ đề Kanji để tải đúng dữ liệu ôn tập từ CSDL."
        title="Kanji theo level"
      />
      <section className="toolbar">
        <SearchInput onChange={setQuery} placeholder="Tìm Kanji, âm đọc, Hán Việt hoặc nghĩa..." value={query} />
        <FilterChips active={topicId} items={topicFilters} onChange={setTopicId} />
      </section>
      {levelQuery.isLoading || topicsQuery.isLoading || kanjiQuery.isLoading ? <SkeletonCard count={6} /> : null}
      {levelQuery.isError || topicsQuery.isError || kanjiQuery.isError ? (
        <ErrorState
          onRetry={() => {
            levelQuery.refetch();
            topicsQuery.refetch();
            kanjiQuery.refetch();
          }}
        />
      ) : null}
      {kanji.length > 0 ? (
        <>
          <section className="kanji-grid">
            {kanji.map((item) => (
              <KanjiCard item={item} key={item.id} />
            ))}
          </section>
          <Pagination onPageChange={setPage} page={page} pageSize={pageSize} total={total} />
        </>
      ) : (
        !kanjiQuery.isLoading && (
          <EmptyState
            actionLabel="Xóa tìm kiếm"
            onAction={() => {
              setQuery("");
              setTopicId("ALL");
            }}
            text="Không có Kanji phù hợp với bộ lọc hiện tại."
            title="Không tìm thấy Kanji"
          />
        )
      )}
    </div>
  );
}
