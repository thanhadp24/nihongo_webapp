import type { ReactNode } from "react";
import { ProgressBar } from "./ProgressBar";

export function PageHeader({
  actions,
  eyebrow,
  progress,
  subtitle,
  title
}: {
  actions?: ReactNode;
  eyebrow?: string;
  progress?: { label: string; value: number };
  subtitle?: string;
  title: string;
}) {
  return (
    <header className="page-header">
      <div>
        {eyebrow ? <p className="eyebrow">{eyebrow}</p> : null}
        <h1>{title}</h1>
        {subtitle ? <p>{subtitle}</p> : null}
      </div>
      {progress ? <ProgressBar label={progress.label} value={progress.value} /> : null}
      {actions ? <div className="page-actions">{actions}</div> : null}
    </header>
  );
}
