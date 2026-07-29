import { useEffect, useMemo, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { ArrowLeft, Image as ImageIcon } from "lucide-react";
import { Link, Navigate, useParams } from "react-router";
import { Breadcrumb } from "../components/common/Breadcrumb";
import { EmptyState, ErrorState, SkeletonCard } from "../components/common/StateViews";
import { PageHeader } from "../components/common/PageHeader";
import { Pagination } from "../components/common/Pagination";
import { SearchInput } from "../components/common/SearchInput";
import { KanjiCard } from "../components/kanji/KanjiCard";
import { KanjiTopicTable } from "../components/kanji/KanjiTopicTable";
import { apiLearningService } from "../services/apiLearningService";

const pageSize = 24;

export function KanjiPage() {
  const { levelId = "n2" } = useParams();
  const [query, setQuery] = useState("");
  const [topicId, setTopicId] = useState<string | null>(null);
  const [page, setPage] = useState(1);

  useEffect(() => {
    setPage(1);
    setTopicId(null);
  }, [levelId]);

  useEffect(() => {
    setPage(1);
  }, [query, topicId]);

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
    queryFn: () =>
      apiLearningService.getKanjiPage(levelId, {
        page,
        pageSize,
        search: query,
        topicId: topicId ?? undefined
      }),
    enabled: Boolean(levelId && (topicId || query))
  });

  const level = levelQuery.data;
  const topics = topicsQuery.data ?? [];
  const kanji = kanjiQuery.data?.items ?? [];
  const total = kanjiQuery.data?.total ?? 0;
  const selectedTopic = useMemo(
    () => topics.find((topic) => topic.id === topicId),
    [topicId, topics]
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
          <Link className="secondary-button" to={`/jlpt/${levelId}/kanji/images`}>
            <ImageIcon aria-hidden="true" />
            Ảnh Kanji
          </Link>
        }
        eyebrow={level?.name ?? "JLPT"}
        subtitle="Kanji được chia theo tuần/ngày. Chọn một chủ đề để tải danh sách Kanji của topic đó."
        title="Kanji theo tuần"
      />
      <section className="toolbar single">
        <SearchInput
          onChange={setQuery}
          placeholder="Tìm Kanji, âm đọc, Hán Việt hoặc nghĩa..."
          value={query}
        />
      </section>
      {levelQuery.isLoading || topicsQuery.isLoading ? <SkeletonCard count={6} /> : null}
      {levelQuery.isError || topicsQuery.isError || kanjiQuery.isError ? (
        <ErrorState
          onRetry={() => {
            levelQuery.refetch();
            topicsQuery.refetch();
            kanjiQuery.refetch();
          }}
        />
      ) : null}

      {!topicId && !query && topics.length > 0 ? (
        <KanjiTopicTable levelId={levelId} topics={topics} onSelect={setTopicId} />
      ) : null}

      {topicId || query ? (
        <>
          <div className="card-title-row">
            <div>
              <p className="eyebrow">{selectedTopic?.sourceWeek ? `Tuần ${selectedTopic.sourceWeek}` : "Danh sách Kanji"}</p>
              <h2>{selectedTopic?.meaning || selectedTopic?.title || "Kết quả tìm kiếm"}</h2>
            </div>
            <button className="secondary-button" onClick={() => {
              setTopicId(null);
              setQuery("");
            }} type="button">
              <ArrowLeft aria-hidden="true" />
              Về bảng tuần
            </button>
          </div>
          {kanjiQuery.isLoading ? <SkeletonCard count={6} /> : null}
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
                actionLabel="Về bảng tuần"
                onAction={() => {
                  setQuery("");
                  setTopicId(null);
                }}
                text="Không có Kanji phù hợp với bộ lọc hiện tại."
                title="Không tìm thấy Kanji"
              />
            )
          )}
        </>
      ) : null}
    </div>
  );
}
