import { Lock, Play } from "lucide-react";
import { Link } from "react-router";
import type { JLPTLevel } from "../../types/learning";
import { actionLabel } from "../../utils/learning";
import { ProgressBar } from "../common/ProgressBar";
import { StatusBadge } from "../common/StatusBadge";

export function JLPTLevelCard({ level }: { level: JLPTLevel }) {
  const isLocked = level.status === "LOCKED";

  const content = (
    <>
      <div className="level-card-top">
        <span className={`level-orb tone-${level.tone}`}>{level.code}</span>
        <StatusBadge status={level.status} />
      </div>
      <div>
        <h2>{level.name}</h2>
        <p className="card-subtitle">{level.subtitle}</p>
        <p>{level.description}</p>
      </div>
      <div className="stat-row">
        <span>{level.chapterCount} Chapters</span>
        <span>{level.topicCount} Chủ đề</span>
        <span>{level.vocabularyCount} Từ vựng</span>
      </div>
      <ProgressBar label="Tiến độ" value={level.progress} />
      <span className={isLocked ? "primary-button disabled" : "primary-button"}>
        {isLocked ? <Lock aria-hidden="true" /> : <Play aria-hidden="true" />}
        {isLocked ? "Hoàn thành N3 để mở khóa" : actionLabel(level.status)}
      </span>
    </>
  );

  if (isLocked) {
    return <article className="level-card locked">{content}</article>;
  }

  return (
    <Link className="level-card" to={`/jlpt/${level.id}`}>
      {content}
    </Link>
  );
}
