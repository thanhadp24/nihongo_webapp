import {
  Bookmark,
  ChevronDown,
  GraduationCap,
  Headphones,
  Home,
  Images,
  Languages,
  LibraryBig,
  MailOpen,
  PenTool,
  Repeat,
  ScrollText,
  SquareStack,
  type LucideIcon
} from "lucide-react";
import { useEffect, useState } from "react";
import { Link, useLocation } from "react-router";

type SidebarItem = {
  id: string;
  to: (levelId: string) => string;
  label: string;
  icon: LucideIcon;
  isActive: (pathname: string) => boolean;
};

const sidebarItems: SidebarItem[] = [
  {
    id: "home",
    to: () => "/",
    label: "Trang chủ",
    icon: Home,
    isActive: (pathname) => pathname === "/"
  },
  {
    id: "jlpt",
    to: () => "/jlpt",
    label: "Lộ trình JLPT",
    icon: GraduationCap,
    isActive: (pathname) =>
      pathname === "/jlpt" ||
      /^\/jlpt\/[^/]+$/.test(pathname) ||
      /^\/jlpt\/[^/]+\/chapters\/[^/]+$/.test(pathname)
  },
  {
    id: "vocabulary",
    to: (levelId) => `/jlpt/${levelId}/vocabulary`,
    label: "Từ vựng",
    icon: LibraryBig,
    isActive: (pathname) =>
      /^\/jlpt\/[^/]+\/vocabulary$/.test(pathname) ||
      pathname.endsWith("/vocabulary")
  },
  {
    id: "grammar",
    to: (levelId) => `/jlpt/${levelId}/grammar`,
    label: "Ngữ pháp",
    icon: PenTool,
    isActive: (pathname) =>
      /^\/jlpt\/[^/]+\/grammar$/.test(pathname) ||
      pathname.endsWith("/lessons") ||
      pathname.startsWith("/lessons/")
  },
  {
    id: "kanji",
    to: (levelId) => `/jlpt/${levelId}/kanji`,
    label: "Kanji",
    icon: Languages,
    isActive: (pathname) => /^\/jlpt\/[^/]+\/kanji$/.test(pathname)
  },
  {
    id: "reading",
    to: () => "/reading",
    label: "Luyện đọc",
    icon: ScrollText,
    isActive: (pathname) => pathname === "/reading"
  },
  {
    id: "listening",
    to: () => "/listening",
    label: "Luyện nghe",
    icon: Headphones,
    isActive: (pathname) => pathname === "/listening"
  },
  {
    id: "review",
    to: () => "/review",
    label: "Ôn tập",
    icon: Repeat,
    isActive: (pathname) => pathname === "/review"
  },
  {
    id: "favorites",
    to: () => "/favorites",
    label: "Nội dung đã lưu",
    icon: Bookmark,
    isActive: (pathname) => pathname === "/favorites"
  }
];

const flashcardItems: SidebarItem[] = [
  {
    id: "flashcard-vocabulary",
    to: (levelId) => `/jlpt/${levelId}/vocabulary/flashcards`,
    label: "Từ vựng",
    icon: LibraryBig,
    isActive: (pathname) =>
      /^\/jlpt\/[^/]+\/vocabulary\/flashcards$/.test(pathname) ||
      /^\/jlpt\/[^/]+\/chapters\/[^/]+\/topics\/[^/]+\/vocabulary\/flashcards$/.test(pathname)
  },
  {
    id: "flashcard-grammar",
    to: (levelId) => `/jlpt/${levelId}/grammar/flashcards`,
    label: "Ngữ pháp",
    icon: PenTool,
    isActive: (pathname) => /^\/jlpt\/[^/]+\/grammar\/flashcards$/.test(pathname)
  },
  {
    id: "flashcard-kanji",
    to: (levelId) => `/jlpt/${levelId}/kanji/flashcards`,
    label: "Kanji",
    icon: Languages,
    isActive: (pathname) => /^\/jlpt\/[^/]+\/kanji\/flashcards$/.test(pathname)
  }
];

const visualItems: SidebarItem[] = [
  {
    id: "visual-kanji",
    to: (levelId) => `/visual/kanji/${levelId}`,
    label: "Theo Kanji",
    icon: Languages,
    isActive: (pathname) => /^\/visual\/kanji\/[^/]+$/.test(pathname)
  },
  {
    id: "visual-letters",
    to: () => "/visual/letters",
    label: "Theo lá thư",
    icon: MailOpen,
    isActive: (pathname) => pathname === "/visual/letters"
  }
];

const flashcardIndex = sidebarItems.findIndex((item) => item.id === "kanji") + 1;
const primaryItems = sidebarItems.slice(0, flashcardIndex);
const secondaryItems = sidebarItems.slice(flashcardIndex);

function SidebarLink({
  currentLevelId,
  item,
  pathname,
  subItem = false
}: {
  currentLevelId: string;
  item: SidebarItem;
  pathname: string;
  subItem?: boolean;
}) {
  const Icon = item.icon;
  const isActive = item.isActive(pathname);

  return (
    <Link
      aria-current={isActive ? "page" : undefined}
      className={["sidebar-link", subItem ? "sidebar-sub-link" : "", isActive ? "active" : ""]
        .filter(Boolean)
        .join(" ")}
      to={item.to(currentLevelId)}
    >
      <Icon aria-hidden="true" />
      <span>{item.label}</span>
    </Link>
  );
}

export function DesktopSidebar({ compact = false }: { compact?: boolean }) {
  const { pathname } = useLocation();
  const currentLevelId =
    pathname.match(/^\/jlpt\/([^/]+)/)?.[1] ??
    pathname.match(/^\/visual\/kanji\/([^/]+)/)?.[1] ??
    "n2";
  const hasActiveFlashcard = flashcardItems.some((item) => item.isActive(pathname));
  const hasActiveVisual = visualItems.some((item) => item.isActive(pathname));
  const [isFlashcardOpen, setIsFlashcardOpen] = useState(hasActiveFlashcard);
  const [isVisualOpen, setIsVisualOpen] = useState(hasActiveVisual);

  useEffect(() => {
    if (hasActiveFlashcard) setIsFlashcardOpen(true);
  }, [hasActiveFlashcard]);

  useEffect(() => {
    if (hasActiveVisual) setIsVisualOpen(true);
  }, [hasActiveVisual]);

  return (
    <aside className={compact ? "desktop-sidebar compact" : "desktop-sidebar"}>
      <nav aria-label="Điều hướng chính">
        {primaryItems.map((item) => (
          <SidebarLink currentLevelId={currentLevelId} item={item} key={item.id} pathname={pathname} />
        ))}

        <button
          aria-expanded={isFlashcardOpen}
          className={hasActiveFlashcard ? "sidebar-link sidebar-expand active" : "sidebar-link sidebar-expand"}
          onClick={() => setIsFlashcardOpen((current) => !current)}
          type="button"
        >
          <SquareStack aria-hidden="true" />
          <span>Flashcard</span>
          <ChevronDown aria-hidden="true" className="sidebar-expand-icon" />
        </button>

        {isFlashcardOpen ? (
          <div className="sidebar-group">
            {flashcardItems.map((item) => (
              <SidebarLink
                currentLevelId={currentLevelId}
                item={item}
                key={item.id}
                pathname={pathname}
                subItem
              />
            ))}
          </div>
        ) : null}

        <button
          aria-expanded={isVisualOpen}
          className={hasActiveVisual ? "sidebar-link sidebar-expand active" : "sidebar-link sidebar-expand"}
          onClick={() => setIsVisualOpen((current) => !current)}
          type="button"
        >
          <Images aria-hidden="true" />
          <span>Học bằng hình ảnh</span>
          <ChevronDown aria-hidden="true" className="sidebar-expand-icon" />
        </button>

        {isVisualOpen ? (
          <div className="sidebar-group">
            {visualItems.map((item) => (
              <SidebarLink
                currentLevelId={currentLevelId}
                item={item}
                key={item.id}
                pathname={pathname}
                subItem
              />
            ))}
          </div>
        ) : null}

        {secondaryItems.map((item) => (
          <SidebarLink currentLevelId={currentLevelId} item={item} key={item.id} pathname={pathname} />
        ))}
      </nav>
    </aside>
  );
}
