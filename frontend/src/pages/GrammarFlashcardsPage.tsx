import { useQuery } from "@tanstack/react-query";
import { Link, Navigate, useParams } from "react-router";
import { Breadcrumb } from "../components/common/Breadcrumb";
import { EmptyState, ErrorState, SkeletonCard } from "../components/common/StateViews";
import { PageHeader } from "../components/common/PageHeader";
import { FlashcardDeck } from "../components/flashcard/FlashcardDeck";
import { apiLearningService } from "../services/apiLearningService";

export function GrammarFlashcardsPage() {
  const { levelId = "n2" } = useParams();
  const levelQuery = useQuery({
    queryKey: ["learning-level", levelId],
    queryFn: () => apiLearningService.getLevel(levelId),
    enabled: Boolean(levelId)
  });
  const cardsQuery = useQuery({
    queryKey: ["learning-flashcard-grammar", levelId],
    queryFn: () => apiLearningService.getGrammarFlashcards(levelId),
    enabled: Boolean(levelId)
  });

  const level = levelQuery.data;
  const cards = cardsQuery.data ?? [];

  if (levelQuery.data === undefined && levelQuery.isSuccess) return <Navigate to="/jlpt" replace />;

  return (
    <div className="page-stack">
      <Breadcrumb
        items={[
          { label: "Trang chủ", to: "/" },
          { label: level?.name ?? levelId.toUpperCase(), to: `/jlpt/${levelId}` },
          { label: "Ngữ pháp", to: `/jlpt/${levelId}/grammar` },
          { label: "Flashcard" }
        ]}
      />
      <PageHeader
        actions={<Link className="secondary-button" to={`/jlpt/${levelId}/grammar`}>Về danh sách</Link>}
        eyebrow={level?.name ?? "JLPT"}
        subtitle="Lật thẻ để tự kiểm tra mẫu câu và ý nghĩa."
        title="Flashcard ngữ pháp"
      />
      {levelQuery.isLoading || cardsQuery.isLoading ? <SkeletonCard count={2} /> : null}
      {levelQuery.isError || cardsQuery.isError ? (
        <ErrorState
          onRetry={() => {
            levelQuery.refetch();
            cardsQuery.refetch();
          }}
        />
      ) : null}
      {cards.length > 0 ? (
        <FlashcardDeck items={cards} />
      ) : (
        !cardsQuery.isLoading && (
          <EmptyState text="Không có ngữ pháp để tạo flashcard." title="Chưa có thẻ ôn tập" />
        )
      )}
    </div>
  );
}
