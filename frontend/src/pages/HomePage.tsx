import { useQuery } from "@tanstack/react-query";
import { ArrowRight, Play } from "lucide-react";
import { Link } from "react-router";
import { JLPTLevelCard } from "../components/jlpt/JLPTLevelCard";
import { PageHeader } from "../components/common/PageHeader";
import { ErrorState, SkeletonCard } from "../components/common/StateViews";
import { apiLearningService } from "../services/apiLearningService";

export function HomePage() {
  const levelsQuery = useQuery({
    queryKey: ["learning-levels"],
    queryFn: apiLearningService.getLevelSummaries
  });
  const n2Level = levelsQuery.data?.find((level) => level.code === "N2");
  const firstReviewLevel = n2Level ?? levelsQuery.data?.[0];

  return (
    <div className="page-stack">
      <section className="hero-panel">
        <div>
          <p className="eyebrow">Chế độ ôn tập</p>
          <h1>Ôn lại JLPT theo dữ liệu trong CSDL</h1>
          <p>
            Bạn đã học tới N2, nên app mở toàn bộ N5-N1. Không còn khóa cấp độ theo tiến độ.
          </p>
        </div>
        <div className="hero-progress">
          <span>Cấp độ ưu tiên</span>
          <strong>{firstReviewLevel?.code ?? "N2"}</strong>
          <Link className="primary-button" to={`/jlpt/${firstReviewLevel?.id ?? "n2"}`}>
            <Play aria-hidden="true" />
            Bắt đầu ôn tập
          </Link>
        </div>
      </section>

      <section className="recent-card">
        <div>
          <p className="eyebrow">Dữ liệu thật</p>
          <h2>{levelsQuery.data ? `${levelsQuery.data.length} cấp độ JLPT đang khả dụng` : "Đang tải dữ liệu"}</h2>
          <p>Chapter, chủ đề, từ vựng và ngữ pháp được đọc qua backend API.</p>
        </div>
        <Link className="secondary-button" to="/jlpt">
          Xem lộ trình
          <ArrowRight aria-hidden="true" />
        </Link>
      </section>

      <PageHeader
        title="Lộ trình học JLPT"
        subtitle="Chọn cấp độ để vào danh sách chapter và bắt đầu ôn tập."
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
