import { useQuery } from "@tanstack/react-query";
import { Navigate, useParams } from "react-router";
import { Breadcrumb } from "../components/common/Breadcrumb";
import { PageHeader } from "../components/common/PageHeader";
import { EmptyState, ErrorState, SkeletonCard } from "../components/common/StateViews";
import { LessonCard } from "../components/lesson/LessonCard";
import { apiLearningService } from "../services/apiLearningService";

export function LessonsPage() {
  const { chapterId = "", levelId = "", topicId = "" } = useParams();
  const pageQuery = useQuery({
    queryKey: ["learning-lessons-page", levelId, chapterId, topicId],
    queryFn: () => apiLearningService.getTopicContext(levelId, chapterId, topicId),
    enabled: Boolean(levelId && chapterId && topicId)
  });
  const lessonsQuery = useQuery({
    queryKey: ["learning-grammar-lessons", levelId],
    queryFn: () => apiLearningService.getLessons(levelId),
    enabled: Boolean(levelId)
  });

  const level = pageQuery.data?.level;
  const chapter = pageQuery.data?.chapter;
  const topic = pageQuery.data?.topic;
  const lessons = lessonsQuery.data ?? [];

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
          { label: "Ngữ pháp" }
        ]}
      />
      <PageHeader
        eyebrow={topic?.title ?? "Chủ đề"}
        subtitle="Bài ngữ pháp được lấy trực tiếp từ CSDL theo cấp độ JLPT."
        title="Danh sách ngữ pháp"
      />
      {pageQuery.isLoading || lessonsQuery.isLoading ? <SkeletonCard count={5} /> : null}
      {pageQuery.isError || lessonsQuery.isError ? (
        <ErrorState onRetry={() => {
          pageQuery.refetch();
          lessonsQuery.refetch();
        }} />
      ) : null}
      {lessons.length > 0 ? (
        <section className="lesson-list">
          {lessons.map((lesson) => (
            <LessonCard key={lesson.id} lesson={lesson} />
          ))}
        </section>
      ) : (
        !lessonsQuery.isLoading && (
          <EmptyState text="Chưa có bài ngữ pháp cho cấp độ này trong CSDL." title="Không có dữ liệu" />
        )
      )}
    </div>
  );
}
