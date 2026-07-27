import { Navigate, useParams } from "react-router";
import { Breadcrumb } from "../components/common/Breadcrumb";
import { PageHeader } from "../components/common/PageHeader";
import { ChapterCard } from "../components/chapter/ChapterCard";
import { learningService } from "../services/learningService";

export function ChaptersPage() {
  const { levelId = "" } = useParams();
  const level = learningService.getLevel(levelId);
  const chapters = learningService.getChapters(levelId);

  if (!level) return <Navigate to="/jlpt" replace />;

  return (
    <div className="page-stack">
      <Breadcrumb
        items={[
          { label: "Trang chủ", to: "/" },
          { label: "Lộ trình JLPT", to: "/jlpt" },
          { label: level.name }
        ]}
      />
      <PageHeader
        eyebrow={level.name}
        progress={{ label: `${level.completedChapters}/${level.chapterCount} Chapters đã hoàn thành`, value: level.progress }}
        subtitle="Nắm vững kiến thức tiếng Nhật cơ bản theo từng chặng nhỏ."
        title={level.name}
      />
      <section className="chapter-list">
        {chapters.map((chapter) => (
          <ChapterCard chapter={chapter} key={chapter.id} />
        ))}
      </section>
    </div>
  );
}
