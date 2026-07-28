import { CheckCircle2, Lock, PlayCircle } from "lucide-react";
import { Link } from "react-router";
import type { Chapter } from "../../types/learning";
import { actionLabel } from "../../utils/learning";
import { StatusBadge } from "../common/StatusBadge";

export function ChapterCard({ chapter }: { chapter: Chapter }) {
  const isLocked = chapter.status === "LOCKED";
  const Icon = chapter.status === "COMPLETED" ? CheckCircle2 : chapter.status === "LOCKED" ? Lock : PlayCircle;

  const content = (
    <>
      <div className="chapter-icon">
        <Icon aria-hidden="true" />
        <span>{String(chapter.chapterNumber).padStart(2, "0")}</span>
      </div>
      <div className="chapter-main">
        <div className="card-title-row">
          <div>
            <p className="eyebrow">Chapter {chapter.chapterNumber}</p>
            <h2>{chapter.title}</h2>
          </div>
          <StatusBadge status={chapter.status} />
        </div>
        <p>{chapter.description}</p>
        <div className="stat-row">
          <span>{chapter.topicCount} Chủ đề</span>
          <span>{chapter.vocabularyCount} Từ vựng</span>
          <span>{chapter.lessonCount} Bài học</span>
        </div>
      </div>
      <div className="chapter-actions">
        <span className={isLocked ? "primary-button disabled" : "primary-button"}>
          {actionLabel(chapter.status)}
        </span>
      </div>
    </>
  );

  if (isLocked) return <article className="chapter-card locked">{content}</article>;

  return (
    <Link className="chapter-card" to={`/jlpt/${chapter.levelId}/chapters/${chapter.id}`}>
      {content}
    </Link>
  );
}
