import { clampProgress } from "../../utils/learning";

export function ProgressBar({ label, value }: { label?: string; value: number }) {
  const progress = clampProgress(value);

  return (
    <div className="progress-block">
      {label ? (
        <div className="progress-label">
          <span>{label}</span>
          <strong>{progress}%</strong>
        </div>
      ) : null}
      <div className="progress-track" aria-label={`Tiến độ ${progress}%`}>
        <span style={{ width: `${progress}%` }} />
      </div>
    </div>
  );
}
