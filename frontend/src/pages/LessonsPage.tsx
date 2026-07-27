import { Navigate, useParams } from "react-router";
import { Breadcrumb } from "../components/common/Breadcrumb";
import { PageHeader } from "../components/common/PageHeader";
import { LessonCard } from "../components/lesson/LessonCard";
import { learningService } from "../services/learningService";

export function LessonsPage() {
  const { chapterId = "", levelId = "", topicId = "" } = useParams();
  const level = learningService.getLevel(levelId);
  const chapter = learningService.getChapter(chapterId);
  const topic = learningService.getTopic(topicId);
  const lessons = learningService.getTopicLessons(topicId);

  if (!level || !chapter || !topic) return <Navigate to="/jlpt" replace />;

  return (
    <div className="page-stack">
      <Breadcrumb
        items={[
          { label: "Trang chủ", to: "/" },
          { label: level.name, to: `/jlpt/${level.id}` },
          { label: topic.title, to: `/jlpt/${level.id}/chapters/${chapter.id}/topics/${topic.id}` },
          { label: "Bài học" }
        ]}
      />
      <PageHeader
        eyebrow={topic.title}
        subtitle="Các bài học được sắp xếp theo thứ tự để bạn đi từ dễ đến khó."
        title="Danh sách bài học"
      />
      <section className="lesson-list">
        {lessons.map((lesson) => (
          <LessonCard key={lesson.id} lesson={lesson} />
        ))}
      </section>
    </div>
  );
}
