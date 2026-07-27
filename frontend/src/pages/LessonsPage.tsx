import { useEffect, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { CreditCard } from "lucide-react";
import { Link, Navigate, useParams } from "react-router";
import { Breadcrumb } from "../components/common/Breadcrumb";
import { PageHeader } from "../components/common/PageHeader";
import { EmptyState, ErrorState, SkeletonCard } from "../components/common/StateViews";
import { Pagination } from "../components/common/Pagination";
import { SearchInput } from "../components/common/SearchInput";
import { GrammarTable } from "../components/grammar/GrammarTable";
import { apiLearningService } from "../services/apiLearningService";

const pageSize = 20;

export function LessonsPage() {
  const { chapterId = "", levelId = "", topicId = "" } = useParams();
  const [query, setQuery] = useState("");
  const [page, setPage] = useState(1);

  useEffect(() => {
    setPage(1);
  }, [levelId, chapterId, topicId, query]);

  const pageQuery = useQuery({
    queryKey: ["learning-lessons-page", levelId, chapterId, topicId],
    queryFn: () => apiLearningService.getTopicContext(levelId, chapterId, topicId),
    enabled: Boolean(levelId && chapterId && topicId)
  });
  const lessonsQuery = useQuery({
    queryKey: ["learning-grammar-lessons", levelId, query, page],
    queryFn: () => apiLearningService.getLessonsPage(levelId, { page, pageSize, search: query }),
    enabled: Boolean(levelId)
  });

  const level = pageQuery.data?.level;
  const chapter = pageQuery.data?.chapter;
  const topic = pageQuery.data?.topic;
  const lessons = lessonsQuery.data?.items ?? [];
  const total = lessonsQuery.data?.total ?? 0;

  if (pageQuery.data && (!level || !chapter || !topic)) return <Navigate to="/jlpt" replace />;

  return (
    <div className="page-stack">
      <Breadcrumb
        items={[
          { label: "Trang chủ", to: "/" },
          { label: level?.name ?? levelId.toUpperCase(), to: `/jlpt/${levelId}` },
          {
            label: topic?.title ?? "Chủ đề",
            to: `/jlpt/${levelId}/chapters/${chapterId}/topics/${topicId}`
          },
          { label: "Ngữ pháp" }
        ]}
      />
      <PageHeader
        actions={
          <>
            <Link className="secondary-button" to={`/jlpt/${levelId}/grammar`}>
              Xem cả level
            </Link>
            <Link className="primary-button" to={`/jlpt/${levelId}/grammar/flashcards`}>
              <CreditCard aria-hidden="true" />
              Flashcard
            </Link>
          </>
        }
        eyebrow={topic?.title ?? "Chủ đề"}
        subtitle="Bài ngữ pháp được lấy trực tiếp từ CSDL theo cấp độ JLPT."
        title="Danh sách ngữ pháp"
      />
      <section className="toolbar single">
        <SearchInput onChange={setQuery} placeholder="Tìm mẫu câu, nghĩa hoặc giải thích..." value={query} />
      </section>
      {pageQuery.isLoading || lessonsQuery.isLoading ? <SkeletonCard count={5} /> : null}
      {pageQuery.isError || lessonsQuery.isError ? (
        <ErrorState
          onRetry={() => {
            pageQuery.refetch();
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
          <EmptyState text="Chưa có bài ngữ pháp cho cấp độ này trong CSDL." title="Không có dữ liệu" />
        )
      )}
    </div>
  );
}
