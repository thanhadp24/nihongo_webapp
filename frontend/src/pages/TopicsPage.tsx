import { useMemo, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Link, Navigate, useParams } from "react-router";
import { Breadcrumb } from "../components/common/Breadcrumb";
import { FilterChips } from "../components/common/FilterChips";
import { PageHeader } from "../components/common/PageHeader";
import { ErrorState, SkeletonCard } from "../components/common/StateViews";
import { TopicCard } from "../components/topic/TopicCard";
import { apiLearningService } from "../services/apiLearningService";
import type { LearningStatus } from "../types/learning";

const filters = [
  { label: "Tất cả", value: "ALL" },
  { label: "Đang ôn", value: "REVIEW_REQUIRED" },
  { label: "Chưa học", value: "NOT_STARTED" },
  { label: "Đã hoàn thành", value: "COMPLETED" }
];

export function TopicsPage() {
  const { chapterId = "", levelId = "" } = useParams();
  const [filter, setFilter] = useState("ALL");
  const topicsQuery = useQuery({
    queryKey: ["learning-topics", levelId, chapterId],
    queryFn: () => apiLearningService.getTopicPage(levelId, chapterId),
    enabled: Boolean(levelId && chapterId)
  });

  const level = topicsQuery.data?.level;
  const chapter = topicsQuery.data?.chapter;
  const topics = topicsQuery.data?.topics ?? [];

  const visibleTopics = useMemo(() => {
    if (filter === "ALL") return topics;
    return topics.filter((topic) => topic.status === filter as LearningStatus);
  }, [filter, topics]);

  if (topicsQuery.data && (!level || !chapter)) return <Navigate to="/jlpt" replace />;

  return (
    <div className="page-stack">
      <Breadcrumb
        items={[
          { label: "Trang chủ", to: "/" },
          { label: level?.name ?? levelId.toUpperCase(), to: `/jlpt/${levelId}` },
          { label: chapter ? `Chapter ${chapter.chapterNumber}` : "Chapter" }
        ]}
      />
      <PageHeader
        actions={
          level && chapter && topics[0] ? (
            <Link className="primary-button" to={`/jlpt/${level.id}/chapters/${chapter.id}/topics/${topics[0].id}`}>
              Bắt đầu ôn tập chủ đề
            </Link>
          ) : null
        }
        eyebrow={chapter ? `Chapter ${chapter.chapterNumber}` : "Chapter"}
        progress={{ label: "Tiến độ ôn tập", value: chapter?.progress ?? 0 }}
        subtitle={
          chapter
            ? `${chapter.topicCount} chủ đề • ${chapter.vocabularyCount} từ vựng`
            : "Đang tải chủ đề từ CSDL"
        }
        title={chapter?.title ?? "Đang tải chapter"}
      />
      <FilterChips active={filter} items={filters} onChange={setFilter} />
      {topicsQuery.isLoading ? <SkeletonCard count={6} /> : null}
      {topicsQuery.isError ? <ErrorState onRetry={() => topicsQuery.refetch()} /> : null}
      {visibleTopics.length > 0 ? (
        <section className="topic-grid">
          {visibleTopics.map((topic) => (
            <TopicCard key={topic.id} topic={topic} />
          ))}
        </section>
      ) : null}
    </div>
  );
}
