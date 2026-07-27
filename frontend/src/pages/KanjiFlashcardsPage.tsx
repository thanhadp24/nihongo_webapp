import { useQuery } from "@tanstack/react-query";
import { Link, Navigate, useParams, useSearchParams } from "react-router";
import { Breadcrumb } from "../components/common/Breadcrumb";
import { EmptyState, ErrorState, SkeletonCard } from "../components/common/StateViews";
import { PageHeader } from "../components/common/PageHeader";
import { FlashcardDeck } from "../components/flashcard/FlashcardDeck";
import { apiLearningService } from "../services/apiLearningService";

export function KanjiFlashcardsPage() {
  const { levelId = "n2" } = useParams();
  const [searchParams] = useSearchParams();
  const topicId = searchParams.get("topicId") ?? undefined;

  const levelQuery = useQuery({
    queryKey: ["learning-level", levelId],
    queryFn: () => apiLearningService.getLevel(levelId),
    enabled: Boolean(levelId)
  });
  const cardsQuery = useQuery({
    queryKey: ["learning-flashcard-kanji", levelId, topicId],
    queryFn: () => apiLearningService.getKanjiFlashcards(levelId, topicId),
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
          { label: "Kanji", to: `/jlpt/${levelId}/kanji` },
          { label: "Flashcard" }
        ]}
      />
      <PageHeader
        actions={<Link className="secondary-button" to={`/jlpt/${levelId}/kanji`}>Về danh sách</Link>}
        eyebrow={level?.name ?? "JLPT"}
        subtitle="Lật thẻ để kiểm tra nghĩa, âm On/Kun và gợi nhớ."
        title="Flashcard Kanji"
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
          <EmptyState text="Không có Kanji để tạo flashcard." title="Chưa có thẻ ôn tập" />
        )
      )}
    </div>
  );
}
