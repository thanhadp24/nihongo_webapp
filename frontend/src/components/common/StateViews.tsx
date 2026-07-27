import { RefreshCw } from "lucide-react";

export function EmptyState({
  actionLabel,
  onAction,
  text,
  title = "Chưa có dữ liệu"
}: {
  actionLabel?: string;
  onAction?: () => void;
  text: string;
  title?: string;
}) {
  return (
    <div className="state-view">
      <strong>{title}</strong>
      <p>{text}</p>
      {actionLabel && onAction ? (
        <button className="secondary-button" onClick={onAction} type="button">
          {actionLabel}
        </button>
      ) : null}
    </div>
  );
}

export function ErrorState({ onRetry }: { onRetry?: () => void }) {
  return (
    <div className="state-view error">
      <strong>Không thể tải dữ liệu.</strong>
      <p>Vui lòng kiểm tra kết nối và thử lại.</p>
      {onRetry ? (
        <button className="secondary-button" onClick={onRetry} type="button">
          <RefreshCw aria-hidden="true" />
          Thử lại
        </button>
      ) : null}
    </div>
  );
}

export function SkeletonCard({ count = 3 }: { count?: number }) {
  return (
    <div className="skeleton-grid" aria-hidden="true">
      {Array.from({ length: count }).map((_, index) => (
        <div className="skeleton-card" key={index}>
          <span />
          <span />
          <span />
        </div>
      ))}
    </div>
  );
}
