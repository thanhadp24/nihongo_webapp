import { useMemo, useState } from "react";
import { Link, Navigate, useParams } from "react-router";
import { Breadcrumb } from "../components/common/Breadcrumb";
import { FilterChips } from "../components/common/FilterChips";
import { PageHeader } from "../components/common/PageHeader";
import { TopicCard } from "../components/topic/TopicCard";
import { learningService } from "../services/learningService";
import type { LearningStatus } from "../types/learning";

const filters = [
  { label: "Tất cả", value: "ALL" },
  { label: "Đang học", value: "IN_PROGRESS" },
  { label: "Chưa học", value: "NOT_STARTED" },
  { label: "Đã hoàn thành", value: "COMPLETED" }
];

export function TopicsPage() {
  const { chapterId = "", levelId = "" } = useParams();
  const [filter, setFilter] = useState("ALL");
  const level = learningService.getLevel(levelId);
  const chapter = learningService.getChapter(chapterId);
  const topics = learningService.getTopics(chapterId);

  const visibleTopics = useMemo(() => {
    if (filter === "ALL") return topics;
    return topics.filter((topic) => topic.status === filter as LearningStatus);
  }, [filter, topics]);

  if (!level || !chapter) return <Navigate to="/jlpt" replace />;

  return (
    <div className="page-stack">
      <Breadcrumb
        items={[
          { label: "Trang chủ", to: "/" },
          { label: level.name, to: `/jlpt/${level.id}` },
          { label: `Chapter ${chapter.chapterNumber}` }
        ]}
      />
      <PageHeader
        actions={
          topics[0] ? (
            <Link className="primary-button" to={`/jlpt/${level.id}/chapters/${chapter.id}/topics/${topics[0].id}`}>
              Tiếp tục nội dung đang học
            </Link>
          ) : null
        }
        eyebrow={`Chapter ${chapter.chapterNumber}`}
        progress={{ label: "Tiến độ Chapter", value: chapter.progress }}
        subtitle={`${chapter.topicCount} chủ đề • ${chapter.vocabularyCount} từ vựng • ${chapter.lessonCount} bài học`}
        title={chapter.title}
      />
      <FilterChips active={filter} items={filters} onChange={setFilter} />
      <section className="topic-grid">
        {visibleTopics.map((topic) => (
          <TopicCard key={topic.id} topic={topic} />
        ))}
      </section>
    </div>
  );
}
