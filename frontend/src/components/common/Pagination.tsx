import { ChevronLeft, ChevronRight } from "lucide-react";

export function Pagination({
  onPageChange,
  page,
  pageSize,
  total
}: {
  onPageChange: (page: number) => void;
  page: number;
  pageSize: number;
  total: number;
}) {
  const totalPages = Math.max(1, Math.ceil(total / pageSize));
  const start = total === 0 ? 0 : (page - 1) * pageSize + 1;
  const end = Math.min(total, page * pageSize);

  if (totalPages <= 1 && total === 0) return null;

  return (
    <nav className="pagination" aria-label="Phân trang">
      <span>
        {start}-{end} / {total}
      </span>
      <div>
        <button
          aria-label="Trang trước"
          className="icon-button"
          disabled={page <= 1}
          onClick={() => onPageChange(page - 1)}
          type="button"
        >
          <ChevronLeft aria-hidden="true" />
        </button>
        <strong>
          {page} / {totalPages}
        </strong>
        <button
          aria-label="Trang sau"
          className="icon-button"
          disabled={page >= totalPages}
          onClick={() => onPageChange(page + 1)}
          type="button"
        >
          <ChevronRight aria-hidden="true" />
        </button>
      </div>
    </nav>
  );
}
