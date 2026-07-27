import { useQuery } from "@tanstack/react-query";
import { Navigate, useParams } from "react-router";
import { Breadcrumb } from "../components/common/Breadcrumb";
import { PageHeader } from "../components/common/PageHeader";
import { ErrorState, SkeletonCard } from "../components/common/StateViews";
import { ChapterCard } from "../components/chapter/ChapterCard";
import { apiLearningService } from "../services/apiLearningService";

export function ChaptersPage() {
  const { levelId = "" } = useParams();
  const chaptersQuery = useQuery({
    queryKey: ["learning-chapters", levelId],
    queryFn: () => apiLearningService.getChaptersPage(levelId),
    enabled: Boolean(levelId)
  });

  if (chaptersQuery.data && !chaptersQuery.data.level) return <Navigate to="/jlpt" replace />;

  const level = chaptersQuery.data?.level;
  const chapters = chaptersQuery.data?.chapters ?? [];

  return (
    <div className="page-stack">
      <Breadcrumb
        items={[
          { label: "Trang chủ", to: "/" },
          { label: "Lộ trình JLPT", to: "/jlpt" },
          { label: level?.name ?? levelId.toUpperCase() }
        ]}
      />
      <PageHeader
        eyebrow={level?.name ?? "JLPT"}
        progress={{
          label: `${chapters.length} Chapters từ CSDL`,
          value: level?.progress ?? 0
        }}
        subtitle="Danh sách chapter được lấy từ bảng chapter/topic của backend."
        title={level?.name ?? "Đang tải level"}
      />
      {chaptersQuery.isLoading ? <SkeletonCard count={4} /> : null}
      {chaptersQuery.isError ? <ErrorState onRetry={() => chaptersQuery.refetch()} /> : null}
      {chapters.length > 0 ? (
        <section className="chapter-list">
          {chapters.map((chapter) => (
            <ChapterCard chapter={chapter} key={chapter.id} />
          ))}
        </section>
      ) : null}
    </div>
  );
}
