import { useQuery } from "@tanstack/react-query";
import { JLPTLevelCard } from "../components/jlpt/JLPTLevelCard";
import { PageHeader } from "../components/common/PageHeader";
import { ErrorState, SkeletonCard } from "../components/common/StateViews";
import { apiLearningService } from "../services/apiLearningService";

export function JLPTLevelsPage() {
  const levelsQuery = useQuery({
    queryKey: ["learning-levels"],
    queryFn: apiLearningService.getLevelSummaries
  });

  return (
    <div className="page-stack">
      <PageHeader
        eyebrow="Lộ trình"
        title="Lộ trình học JLPT"
        subtitle="Dữ liệu được lấy từ CSDL. Tất cả cấp độ đều mở để phục vụ ôn tập."
      />
      {levelsQuery.isLoading ? <SkeletonCard count={5} /> : null}
      {levelsQuery.isError ? <ErrorState onRetry={() => levelsQuery.refetch()} /> : null}
      {levelsQuery.data ? (
        <section className="level-grid">
          {levelsQuery.data.map((level) => (
            <JLPTLevelCard key={level.id} level={level} />
          ))}
        </section>
      ) : null}
    </div>
  );
}
