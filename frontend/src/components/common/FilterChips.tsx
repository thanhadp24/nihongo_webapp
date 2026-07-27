export type FilterChip = {
  label: string;
  value: string;
};

export function FilterChips({
  active,
  items,
  onChange
}: {
  active: string;
  items: FilterChip[];
  onChange: (value: string) => void;
}) {
  return (
    <div className="filter-chips" aria-label="Bộ lọc">
      {items.map((item) => (
        <button
          className={item.value === active ? "filter-chip active" : "filter-chip"}
          key={item.value}
          onClick={() => onChange(item.value)}
          type="button"
        >
          {item.label}
        </button>
      ))}
    </div>
  );
}
