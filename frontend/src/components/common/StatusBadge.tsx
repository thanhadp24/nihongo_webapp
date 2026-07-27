import type { LearningStatus } from "../../types/learning";
import { statusLabels } from "../../utils/learning";

export function StatusBadge({ status }: { status: LearningStatus }) {
  return <span className={`status-badge status-${status.toLowerCase()}`}>{statusLabels[status]}</span>;
}
