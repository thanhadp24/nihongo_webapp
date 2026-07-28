import { Bell, Menu, Search, UserRound } from "lucide-react";
import { useState } from "react";
import { useLocation } from "react-router";
import { LevelSelector } from "../common/LevelSelector";
import { SearchInput } from "../common/SearchInput";

function pathForLevel(pathname: string, nextLevel: string) {
  if (/^\/jlpt\/[^/]+\/vocabulary\/flashcards/.test(pathname)) {
    return `/jlpt/${nextLevel}/vocabulary/flashcards`;
  }

  if (/^\/jlpt\/[^/]+\/grammar\/flashcards/.test(pathname)) {
    return `/jlpt/${nextLevel}/grammar/flashcards`;
  }

  if (/^\/jlpt\/[^/]+\/kanji\/flashcards/.test(pathname)) {
    return `/jlpt/${nextLevel}/kanji/flashcards`;
  }

  if (/^\/jlpt\/[^/]+\/chapters\/[^/]+\/topics\/[^/]+\/vocabulary/.test(pathname)) {
    return `/jlpt/${nextLevel}/vocabulary`;
  }

  if (/^\/jlpt\/[^/]+\/chapters\/[^/]+\/topics\/[^/]+\/lessons/.test(pathname)) {
    return `/jlpt/${nextLevel}/grammar`;
  }

  if (/^\/jlpt\/[^/]+\/vocabulary/.test(pathname)) return `/jlpt/${nextLevel}/vocabulary`;
  if (/^\/jlpt\/[^/]+\/grammar/.test(pathname) || pathname.startsWith("/lessons/")) {
    return `/jlpt/${nextLevel}/grammar`;
  }
  if (/^\/jlpt\/[^/]+\/kanji/.test(pathname) || pathname.startsWith("/kanji/")) {
    return `/jlpt/${nextLevel}/kanji`;
  }

  return `/jlpt/${nextLevel}`;
}

export function AppHeader({ onMenuClick }: { onMenuClick: () => void }) {
  const { pathname } = useLocation();
  const [query, setQuery] = useState("");
  const [isSearchOpen, setIsSearchOpen] = useState(false);
  const currentLevelId = pathname.match(/^\/jlpt\/([^/]+)/)?.[1] ?? "n2";

  return (
    <header className="app-header">
      <div className="brand-row">
        <button aria-label="Mở menu" className="icon-button menu-button" onClick={onMenuClick} type="button">
          <Menu aria-hidden="true" />
        </button>
        <span className="brand-mark" aria-hidden="true">日</span>
        <div>
          <strong>Nihongo Learning</strong>
          <span>JLPT Study Desk</span>
        </div>
      </div>

      <div className="header-search">
        <SearchInput
          compact
          onChange={setQuery}
          placeholder="Tìm từ vựng, Kanji, ngữ pháp, bài học..."
          value={query}
        />
      </div>

      <div className="header-level-selector">
        <LevelSelector
          label="JLPT"
          value={currentLevelId}
          toForLevel={(nextLevel) => pathForLevel(pathname, nextLevel)}
        />
      </div>

      <div className="header-actions">
        <button
          aria-label="Mở tìm kiếm"
          className="icon-button mobile-search-button"
          onClick={() => setIsSearchOpen(true)}
          type="button"
        >
          <Search aria-hidden="true" />
        </button>
        <button aria-label="Thông báo" className="icon-button" type="button">
          <Bell aria-hidden="true" />
        </button>

        <button aria-label="Tài khoản" className="avatar-button" type="button">
          <UserRound aria-hidden="true" />
        </button>
      </div>

      {isSearchOpen ? (
        <div className="mobile-search-overlay">
          <SearchInput
            onChange={setQuery}
            placeholder="Tìm bằng tiếng Nhật, Hiragana, Romaji hoặc nghĩa..."
            value={query}
          />
          <button className="secondary-button" onClick={() => setIsSearchOpen(false)} type="button">
            Đóng
          </button>
        </div>
      ) : null}
    </header>
  );
}
