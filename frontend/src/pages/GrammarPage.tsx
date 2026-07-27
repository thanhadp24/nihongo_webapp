import { useEffect, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { CreditCard } from "lucide-react";
import { Link, Navigate, useParams } from "react-router";
import { Breadcrumb } from "../components/common/Breadcrumb";
import { EmptyState, ErrorState, SkeletonCard } from "../components/common/StateViews";
import { LevelSelector } from "../components/common/LevelSelector";
import { PageHeader } from "../components/common/PageHeader";
import { Pagination } from "../components/common/Pagination";
import { SearchInput } from "../components/common/SearchInput";
import { GrammarTable } from "../components/grammar/GrammarTable";
import { apiLearningService } from "../services/apiLearningService";

const pageSize = 20;

export function GrammarPage() {
  const { levelId = "n2" } = useParams();
  const [query, setQuery] = useState("");
  const [page, setPage] = useState(1);

  useEffect(() => {
    setPage(1);
  }, [levelId, query]);

  const levelQuery = useQuery({
    queryKey: ["learning-level", levelId],
    queryFn: () => apiLearningService.getLevel(levelId),
    enabled: Boolean(levelId)
  });
  const lessonsQuery = useQuery({
    queryKey: ["learning-grammar-page", levelId, query, page],
    queryFn: () => apiLearningService.getLessonsPage(levelId, { page, pageSize, search: query }),
    enabled: Boolean(levelId)
  });

  const level = levelQuery.data;
  const lessons = lessonsQuery.data?.items ?? [];
  const total = lessonsQuery.data?.total ?? 0;

  if (levelQuery.data === undefined && levelQuery.isSuccess) return <Navigate to="/jlpt" replace />;

  return (
    <div className="page-stack">
      <Breadcrumb
        items={[
          { label: "Trang chủ", to: "/" },
          { label: level?.name ?? levelId.toUpperCase(), to: `/jlpt/${levelId}` },
          { label: "Ngữ pháp" }
        ]}
      />
      <PageHeader
        actions={
          <>
            <LevelSelector value={levelId} toForLevel={(nextLevel) => `/jlpt/${nextLevel}/grammar`} />
            <Link className="primary-button" to={`/jlpt/${levelId}/grammar/flashcards`}>
              <CreditCard aria-hidden="true" />
              Flashcard
            </Link>
          </>
        }
        eyebrow={level?.name ?? "JLPT"}
        subtitle="Chọn level để tải mẫu ngữ pháp đúng cấp độ từ CSDL."
        title="Ngữ pháp theo level"
      />
      <section className="toolbar single">
        <SearchInput onChange={setQuery} placeholder="Tìm mẫu câu, nghĩa hoặc giải thích..." value={query} />
      </section>
      {levelQuery.isLoading || lessonsQuery.isLoading ? <SkeletonCard count={5} /> : null}
      {levelQuery.isError || lessonsQuery.isError ? (
        <ErrorState
          onRetry={() => {
            levelQuery.refetch();
            lessonsQuery.refetch();
          }}
        />
      ) : null}
      {lessons.length > 0 ? (
        <>
          <GrammarTable lessons={lessons} />
          <Pagination onPageChange={setPage} page={page} pageSize={pageSize} total={total} />
        </>
      ) : (
        !lessonsQuery.isLoading && (
          <EmptyState
            actionLabel="Xóa tìm kiếm"
            onAction={() => setQuery("")}
            text="Không có mẫu ngữ pháp phù hợp với bộ lọc hiện tại."
            title="Không tìm thấy ngữ pháp"
          />
        )
      )}
    </div>
  );
}
