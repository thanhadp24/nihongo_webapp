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
import { VocabularyCard } from "../components/vocabulary/VocabularyCard";
import { apiLearningService } from "../services/apiLearningService";

const pageSize = 24;

export function LevelVocabularyPage() {
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
  const wordsQuery = useQuery({
    queryKey: ["learning-level-vocabulary", levelId, query, page],
    queryFn: () => apiLearningService.getLevelVocabularyPage(levelId, { page, pageSize, search: query }),
    enabled: Boolean(levelId)
  });

  const level = levelQuery.data;
  const words = wordsQuery.data?.items ?? [];
  const total = wordsQuery.data?.total ?? 0;

  if (levelQuery.data === undefined && levelQuery.isSuccess) return <Navigate to="/jlpt" replace />;

  return (
    <div className="page-stack">
      <Breadcrumb
        items={[
          { label: "Trang chủ", to: "/" },
          { label: level?.name ?? levelId.toUpperCase(), to: `/jlpt/${levelId}` },
          { label: "Từ vựng" }
        ]}
      />
      <PageHeader
        actions={
          <>
            <LevelSelector value={levelId} toForLevel={(nextLevel) => `/jlpt/${nextLevel}/vocabulary`} />
            <Link className="primary-button" to={`/jlpt/${levelId}/vocabulary/flashcards`}>
              <CreditCard aria-hidden="true" />
              Flashcard
            </Link>
          </>
        }
        eyebrow={level?.name ?? "JLPT"}
        subtitle="Chọn level để tải danh sách từ vựng tương ứng trực tiếp từ CSDL."
        title="Từ vựng theo level"
      />
      <section className="toolbar single">
        <SearchInput onChange={setQuery} placeholder="Tìm từ, cách đọc hoặc nghĩa..." value={query} />
      </section>
      {levelQuery.isLoading || wordsQuery.isLoading ? <SkeletonCard count={6} /> : null}
      {levelQuery.isError || wordsQuery.isError ? (
        <ErrorState
          onRetry={() => {
            levelQuery.refetch();
            wordsQuery.refetch();
          }}
        />
      ) : null}
      {words.length > 0 ? (
        <>
          <section className="vocabulary-grid-cards">
            {words.map((word) => (
              <VocabularyCard item={word} key={word.id} />
            ))}
          </section>
          <Pagination onPageChange={setPage} page={page} pageSize={pageSize} total={total} />
        </>
      ) : (
        !wordsQuery.isLoading && (
          <EmptyState
            actionLabel="Xóa tìm kiếm"
            onAction={() => setQuery("")}
            text="Không có từ vựng phù hợp với bộ lọc hiện tại."
            title="Không tìm thấy từ vựng"
          />
        )
      )}
    </div>
  );
}
