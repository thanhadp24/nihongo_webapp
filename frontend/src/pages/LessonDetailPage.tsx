import { useQuery } from "@tanstack/react-query";
import { ArrowLeft, CheckCircle2, Volume2 } from "lucide-react";
import { Link, Navigate, useParams } from "react-router";
import { PageHeader } from "../components/common/PageHeader";
import { ErrorState, SkeletonCard } from "../components/common/StateViews";
import { apiLearningService } from "../services/apiLearningService";
import { speakJapanese } from "../utils/speech";

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
    <div className="page-stack">
      {lessonQuery.isLoading ? <SkeletonCard count={2} /> : null}
      {lessonQuery.isError ? <ErrorState onRetry={() => lessonQuery.refetch()} /> : null}
      {lesson ? (
        <>
          <PageHeader
            actions={
              <button
                className="secondary-button"
                onClick={() => speakJapanese(detail?.pattern ?? lesson.japaneseTitle)}
                type="button"
              >
                <Volume2 aria-hidden="true" />
                Nghe mẫu
              </button>
            }
            eyebrow={detail?.chapter_name ?? "Ngữ pháp"}
            subtitle={detail?.meaning_vi ?? lesson.meaning}
            title={detail?.pattern ?? lesson.japaneseTitle}
          />

          <section className="grammar-detail-table-wrap">
            <table className="grammar-detail-table">
              <tbody>
                <tr>
                  <th>Mẫu</th>
                  <td>{detail?.pattern ?? lesson.japaneseTitle}</td>
                </tr>
                <tr>
                  <th>Nghĩa</th>
                  <td>{detail?.meaning_vi ?? lesson.meaning}</td>
                </tr>
                <tr>
                  <th>Cấu trúc</th>
                  <td>{detail?.formation || lesson.formation || "Chưa có dữ liệu cấu trúc."}</td>
                </tr>
                <tr>
                  <th>Giải thích</th>
                  <td>{detail?.explanation || lesson.explanation || "Chưa có dữ liệu giải thích."}</td>
                </tr>
              </tbody>
            </table>
          </section>

          {examples.length > 0 ? (
            <section className="grammar-examples-panel">
              <div className="card-title-row">
                <div>
                  <p className="eyebrow">Ví dụ</p>
                  <h2>Câu mẫu trong CSDL</h2>
                </div>
              </div>
              {examples.map((example) => (
                <article className="grammar-example-row" key={example.id}>
                  <button
                    aria-label="Nghe ví dụ"
                    className="icon-button"
                    onClick={() => speakJapanese(example.japanese_text)}
                    type="button"
                  >
                    <Volume2 aria-hidden="true" />
                  </button>
                  <div>
                    <p className="example-jp">{example.japanese_text}</p>
                    {example.reading ? <p>{example.reading}</p> : null}
                    {example.meaning_vi ? <p>{example.meaning_vi}</p> : null}
                  </div>
                </article>
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
            </button>
          </div>
        </>
      ) : null}
    </div>
  );
}
