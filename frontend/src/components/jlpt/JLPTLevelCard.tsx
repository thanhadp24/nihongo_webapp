import { Play } from "lucide-react";
import { Link } from "react-router";
import type { JLPTLevel } from "../../types/learning";
import { actionLabel } from "../../utils/learning";
import { ProgressBar } from "../common/ProgressBar";
import { StatusBadge } from "../common/StatusBadge";

export function JLPTLevelCard({ level }: { level: JLPTLevel }) {
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
      <span className="primary-button">
        <Play aria-hidden="true" />
        {actionLabel(level.status)}
      </span>
    </>
  );

  return (
    <Link className="level-card" to={`/jlpt/${level.id}`}>
      {content}
    </Link>
  );
}
