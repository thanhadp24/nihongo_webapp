import { ArrowLeft, ArrowRight, CheckCircle2, ListTree, Volume2 } from "lucide-react";
import { Link, Navigate, useParams } from "react-router";
import { PageHeader } from "../components/common/PageHeader";
import { ProgressBar } from "../components/common/ProgressBar";
import { learningService } from "../services/learningService";

export function LessonDetailPage() {
  const { lessonId = "" } = useParams();
  const lesson = learningService.getLesson(lessonId);
  const topic = lesson ? learningService.getTopic(lesson.topicId) : undefined;

  if (!lesson || !topic) return <Navigate to="/jlpt" replace />;

  return (
    <div className="learning-layout">
      <aside className="lesson-outline">
        <strong>Nội dung bài học</strong>
        {["Giới thiệu", "Từ vựng", "Mẫu câu", "Hội thoại", "Luyện tập", "Tổng kết"].map((item, index) => (
          <a className={index === 1 ? "active" : ""} href={`#section-${index + 1}`} key={item}>
            {index + 1}. {item}
          </a>
        ))}
      </aside>
      <article className="lesson-reader">
        <PageHeader
          eyebrow={topic.title}
          progress={{ label: "Tiến độ bài học", value: lesson.progress }}
          subtitle={lesson.japaneseTitle}
          title={lesson.title}
        />
        <section className="study-focus-card">
          <button className="secondary-button" type="button">
            <Volume2 aria-hidden="true" />
            Nghe phát âm
          </button>
          <h2>おはようございます</h2>
          <p className="japanese-caption">Chào buổi sáng một cách lịch sự.</p>
          <p>
            Cụm từ này thường dùng vào buổi sáng khi gặp giáo viên, đồng nghiệp hoặc người lớn tuổi.
            Khi nói với bạn bè thân thiết, bạn có thể dùng dạng ngắn hơn: おはよう.
          </p>
        </section>
        <section className="example-box large">
          <span>Ví dụ hội thoại</span>
          <p className="example-jp">A: おはようございます。 B: おはようございます。</p>
          <p>A: Chào buổi sáng. B: Chào buổi sáng.</p>
        </section>
        <div className="lesson-bottom-actions">
          <Link className="secondary-button" to={`/jlpt/${topic.levelId}/chapters/${topic.chapterId}/topics/${topic.id}/lessons`}>
            <ArrowLeft aria-hidden="true" />
            Bài trước
          </Link>
          <button className="primary-button" type="button">
            <CheckCircle2 aria-hidden="true" />
            Hoàn thành và tiếp tục
            <ArrowRight aria-hidden="true" />
          </button>
        </div>
      </article>
      <aside className="lesson-note-panel">
        <ListTree aria-hidden="true" />
        <strong>Ghi chú nhanh</strong>
        <p>12/20 nội dung đã hoàn thành. Bài tiếp theo: Chào hỏi lịch sự.</p>
        <ProgressBar value={60} />
      </aside>
    </div>
  );
}
