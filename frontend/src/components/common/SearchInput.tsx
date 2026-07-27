import { Search, X } from "lucide-react";

export function SearchInput({
  compact = false,
  onChange,
  placeholder,
  value
}: {
  compact?: boolean;
  onChange: (value: string) => void;
  placeholder: string;
  value: string;
}) {
  return (
    <label className={compact ? "search-input compact" : "search-input"}>
      <span>Tìm kiếm</span>
      <div>
        <Search aria-hidden="true" />
        <input
          onChange={(event) => onChange(event.target.value)}
          placeholder={placeholder}
          value={value}
        />
        {value ? (
          <button aria-label="Xóa tìm kiếm" onClick={() => onChange("")} type="button">
            <X aria-hidden="true" />
          </button>
        ) : null}
      </div>
    </label>
  );
}
