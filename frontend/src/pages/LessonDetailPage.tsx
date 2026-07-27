import { useQuery } from "@tanstack/react-query";
import { ArrowLeft, ArrowRight, CheckCircle2, ListTree, Volume2 } from "lucide-react";
import { Link, Navigate, useParams } from "react-router";
import { PageHeader } from "../components/common/PageHeader";
import { ProgressBar } from "../components/common/ProgressBar";
import { ErrorState, SkeletonCard } from "../components/common/StateViews";
import { apiLearningService } from "../services/apiLearningService";

export function LessonDetailPage() {
  const { lessonId = "" } = useParams();
  const lessonQuery = useQuery({
    queryKey: ["learning-grammar-detail", lessonId],
    queryFn: () => apiLearningService.getLessonDetail(lessonId),
    enabled: Boolean(lessonId)
  });

  if (lessonQuery.data && !lessonQuery.data.lesson) return <Navigate to="/jlpt" replace />;

  const lesson = lessonQuery.data?.lesson;
  const detail = lessonQuery.data?.detail;
  const examples = detail?.examples ?? [];

  return (
    <div className="learning-layout">
      <aside className="lesson-outline">
        <strong>Nội dung bài học</strong>
        {["Mẫu câu", "Cấu trúc", "Giải thích", "Ví dụ", "Ôn tập"].map((item, index) => (
          <a className={index === 0 ? "active" : ""} href={`#section-${index + 1}`} key={item}>
            {index + 1}. {item}
          </a>
        ))}
      </aside>
      <article className="lesson-reader">
        {lessonQuery.isLoading ? <SkeletonCard count={2} /> : null}
        {lessonQuery.isError ? <ErrorState onRetry={() => lessonQuery.refetch()} /> : null}
        {lesson ? (
          <>
            <PageHeader
              eyebrow={detail?.chapter_name ?? "Ngữ pháp"}
              progress={{ label: "Tiến độ ôn tập", value: lesson.progress }}
              subtitle={lesson.japaneseTitle}
              title={lesson.title}
            />
            <section className="study-focus-card" id="section-1">
              <button className="secondary-button" type="button">
                <Volume2 aria-hidden="true" />
                Nghe phát âm
              </button>
              <h2>{detail?.pattern ?? lesson.japaneseTitle}</h2>
              <p className="japanese-caption">{detail?.meaning_vi ?? lesson.title}</p>
              {detail?.formation ? <p id="section-2">{detail.formation}</p> : null}
              {detail?.explanation ? <p id="section-3">{detail.explanation}</p> : null}
            </section>
            {examples.length > 0 ? (
              <section className="example-box large" id="section-4">
                <span>Ví dụ</span>
                {examples.map((example) => (
                  <div key={example.id}>
                    <p className="example-jp">{example.japanese_text}</p>
                    {example.reading ? <p>{example.reading}</p> : null}
                    {example.meaning_vi ? <p>{example.meaning_vi}</p> : null}
                  </div>
                ))}
              </section>
            ) : null}
            <div className="lesson-bottom-actions">
              <Link className="secondary-button" to="/jlpt">
                <ArrowLeft aria-hidden="true" />
                Về lộ trình
              </Link>
              <button className="primary-button" type="button">
                <CheckCircle2 aria-hidden="true" />
                Hoàn thành ôn tập
                <ArrowRight aria-hidden="true" />
              </button>
            </div>
          </>
        ) : null}
      </article>
      <aside className="lesson-note-panel">
        <ListTree aria-hidden="true" />
        <strong>Ghi chú nhanh</strong>
        <p>Dữ liệu bài học đang đọc từ endpoint ngữ pháp chi tiết của backend.</p>
        <ProgressBar value={lesson?.progress ?? 0} />
      </aside>
    </div>
  );
}
