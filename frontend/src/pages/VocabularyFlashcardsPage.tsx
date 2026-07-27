import { useQuery } from "@tanstack/react-query";
import { Link, Navigate, useParams } from "react-router";
import { Breadcrumb } from "../components/common/Breadcrumb";
import { EmptyState, ErrorState, SkeletonCard } from "../components/common/StateViews";
import { PageHeader } from "../components/common/PageHeader";
import { FlashcardDeck } from "../components/flashcard/FlashcardDeck";
import { apiLearningService } from "../services/apiLearningService";

export function VocabularyFlashcardsPage() {
  const { chapterId, levelId = "n2", topicId } = useParams();
  const contextQuery = useQuery({
    queryKey: ["learning-flashcard-vocabulary-context", levelId, chapterId, topicId],
    queryFn: () =>
      chapterId && topicId
        ? apiLearningService.getTopicContext(levelId, chapterId, topicId)
        : apiLearningService.getLevel(levelId).then((level) => ({ level, chapter: undefined, topic: undefined })),
    enabled: Boolean(levelId)
  });
  const cardsQuery = useQuery({
    queryKey: ["learning-flashcard-vocabulary", levelId, chapterId, topicId],
    queryFn: () => apiLearningService.getVocabularyFlashcards(levelId, chapterId, topicId),
    enabled: Boolean(levelId)
  });

  const level = contextQuery.data?.level;
  const topic = contextQuery.data?.topic;
  const cards = cardsQuery.data ?? [];

  if (contextQuery.data && !level) return <Navigate to="/jlpt" replace />;

  return (
    <div className="page-stack">
      <Breadcrumb
        items={[
          { label: "Trang chủ", to: "/" },
          { label: level?.name ?? levelId.toUpperCase(), to: `/jlpt/${levelId}` },
          {
            label: "Từ vựng",
            to:
              chapterId && topicId
                ? `/jlpt/${levelId}/chapters/${chapterId}/topics/${topicId}/vocabulary`
                : `/jlpt/${levelId}/vocabulary`
          },
          { label: "Flashcard" }
        ]}
      />
      <PageHeader
        actions={
          <Link
            className="secondary-button"
            to={
              chapterId && topicId
                ? `/jlpt/${levelId}/chapters/${chapterId}/topics/${topicId}/vocabulary`
                : `/jlpt/${levelId}/vocabulary`
            }
          >
            Về danh sách
          </Link>
        }
        eyebrow={topic?.title ?? level?.name ?? "JLPT"}
        subtitle="Lật thẻ để kiểm tra nghĩa, cách đọc và ví dụ."
        title="Flashcard từ vựng"
      />
      {contextQuery.isLoading || cardsQuery.isLoading ? <SkeletonCard count={2} /> : null}
      {contextQuery.isError || cardsQuery.isError ? (
        <ErrorState
          onRetry={() => {
            contextQuery.refetch();
            cardsQuery.refetch();
          }}
        />
      ) : null}
      {cards.length > 0 ? (
        <FlashcardDeck items={cards} />
      ) : (
        !cardsQuery.isLoading && (
          <EmptyState text="Không có từ vựng để tạo flashcard." title="Chưa có thẻ ôn tập" />
        )
      )}
    </div>
  );
}
