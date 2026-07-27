import { ChevronRight } from "lucide-react";
import { Link } from "react-router";

export type BreadcrumbItem = {
  label: string;
  to?: string;
};

export function Breadcrumb({ items }: { items: BreadcrumbItem[] }) {
  return (
    <nav className="breadcrumb" aria-label="Breadcrumb">
      {items.map((item, index) => (
        <span key={`${item.label}-${index}`} className="breadcrumb-item">
          {item.to ? <Link to={item.to}>{item.label}</Link> : <strong>{item.label}</strong>}
          {index < items.length - 1 ? <ChevronRight aria-hidden="true" /> : null}
        </span>
      ))}
    </nav>
  );
}
