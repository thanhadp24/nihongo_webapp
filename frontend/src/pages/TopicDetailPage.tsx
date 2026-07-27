import { useQuery } from "@tanstack/react-query";
import { BookOpen, Dumbbell, Languages, LibraryBig } from "lucide-react";
import { Link, Navigate, useParams } from "react-router";
import { Breadcrumb } from "../components/common/Breadcrumb";
import { PageHeader } from "../components/common/PageHeader";
import { ProgressBar } from "../components/common/ProgressBar";
import { ErrorState, SkeletonCard } from "../components/common/StateViews";
import { apiLearningService } from "../services/apiLearningService";

export function TopicDetailPage() {
  const { chapterId = "", levelId = "", topicId = "" } = useParams();
  const topicQuery = useQuery({
    queryKey: ["learning-topic-detail", levelId, chapterId, topicId],
    queryFn: async () => {
      const [context, vocabulary, lessons] = await Promise.all([
        apiLearningService.getTopicContext(levelId, chapterId, topicId),
        apiLearningService.getTopicVocabulary(levelId, chapterId, topicId),
        apiLearningService.getLessons(levelId)
      ]);

      return { ...context, vocabulary, lessons };
    },
    enabled: Boolean(levelId && chapterId && topicId)
  });

  if (topicQuery.data && (!topicQuery.data.level || !topicQuery.data.chapter || !topicQuery.data.topic)) {
    return <Navigate to="/jlpt" replace />;
  }

  const level = topicQuery.data?.level;
  const chapter = topicQuery.data?.chapter;
  const topic = topicQuery.data?.topic;
  const topicVocabulary = topicQuery.data?.vocabulary ?? [];
  const topicLessons = topicQuery.data?.lessons ?? [];

  return (
    <div className="page-stack">
      <Breadcrumb
        items={[
          { label: "Trang chủ", to: "/" },
          { label: level?.name ?? levelId.toUpperCase(), to: `/jlpt/${levelId}` },
          {
            label: chapter ? `Chapter ${chapter.chapterNumber}` : "Chapter",
            to: `/jlpt/${levelId}/chapters/${chapterId}`
          },
          { label: topic?.title ?? "Chủ đề" }
        ]}
      />
      <PageHeader
        actions={
          topic ? (
            <Link className="primary-button" to={`/jlpt/${levelId}/chapters/${chapterId}/topics/${topic.id}/vocabulary`}>
              Ôn tập từ vựng
            </Link>
          ) : null
        }
        eyebrow={`${level?.name ?? "JLPT"} - ${chapter ? `Chapter ${chapter.chapterNumber}` : "Chapter"}`}
        subtitle={topic?.description ?? "Đang tải dữ liệu chủ đề từ CSDL."}
        title={topic?.title ?? "Đang tải chủ đề"}
      />
      {topicQuery.isLoading ? <SkeletonCard count={2} /> : null}
      {topicQuery.isError ? <ErrorState onRetry={() => topicQuery.refetch()} /> : null}
      {topic ? (
        <section className="topic-overview">
          <div className="overview-main">
            <p className="japanese-title-small">{topic.japaneseTitle}</p>
            <div className="stat-row roomy">
              <span><LibraryBig aria-hidden="true" /> {topicVocabulary.length} từ vựng</span>
              <span><BookOpen aria-hidden="true" /> {topicLessons.length} bài ngữ pháp</span>
              <span><Languages aria-hidden="true" /> Kanji theo level</span>
              <span><Dumbbell aria-hidden="true" /> Ôn tập mở</span>
            </div>
            <ProgressBar label="Tiến độ ôn tập chủ đề" value={topic.progress} />
          </div>
          <div className="content-tabs">
            <Link to={`/jlpt/${levelId}/chapters/${chapterId}/topics/${topic.id}`}>Tổng quan</Link>
            <Link to={`/jlpt/${levelId}/chapters/${chapterId}/topics/${topic.id}/vocabulary`}>Từ vựng</Link>
            <Link to={`/jlpt/${levelId}/grammar`}>Ngữ pháp</Link>
            <Link to={`/jlpt/${levelId}/kanji`}>Kanji</Link>
          </div>
        </section>
      ) : null}
    </div>
  );
}
