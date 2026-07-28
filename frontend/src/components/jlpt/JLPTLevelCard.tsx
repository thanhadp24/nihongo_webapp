import { Play } from "lucide-react";
import { Link } from "react-router";
import type { JLPTLevel } from "../../types/learning";
import { actionLabel } from "../../utils/learning";

export function JLPTLevelCard({ level }: { level: JLPTLevel }) {
  const content = (
    <>
      <div className="level-card-top">
        <span className={`level-orb tone-${level.tone}`}>{level.code}</span>
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
