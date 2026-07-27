import {
  BarChart3,
  Bookmark,
  BookOpen,
  GraduationCap,
  Headphones,
  Home,
  Languages,
  LibraryBig,
  PenTool,
  Repeat,
  ScrollText
} from "lucide-react";
import { NavLink } from "react-router";
import { ProgressBar } from "../common/ProgressBar";

const sidebarItems = [
  { to: "/", label: "Trang chủ", icon: Home },
  { to: "/jlpt", label: "Lộ trình JLPT", icon: GraduationCap },
  { to: "/jlpt/n5/chapters/n5-c1/topics/n5-c1-t1/vocabulary", label: "Từ vựng", icon: LibraryBig },
  { to: "/jlpt/n5/chapters/n5-c1/topics/n5-c1-t1/lessons", label: "Ngữ pháp", icon: PenTool },
  { to: "/jlpt/n5/chapters/n5-c1/topics/n5-c1-t1", label: "Kanji", icon: Languages },
  { to: "/review", label: "Luyện đọc", icon: ScrollText },
  { to: "/review", label: "Luyện nghe", icon: Headphones },
  { to: "/review", label: "Ôn tập", icon: Repeat },
  { to: "/favorites", label: "Nội dung đã lưu", icon: Bookmark },
  { to: "/progress", label: "Tiến độ học", icon: BarChart3 }
];

export function DesktopSidebar({ compact = false }: { compact?: boolean }) {
  return (
    <aside className={compact ? "desktop-sidebar compact" : "desktop-sidebar"}>
      <nav aria-label="Điều hướng chính">
        {sidebarItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink className="sidebar-link" key={`${item.to}-${item.label}`} to={item.to}>
              <Icon aria-hidden="true" />
              <span>{item.label}</span>
            </NavLink>
          );
        })}
      </nav>

      <section className="daily-goal">
        <BookOpen aria-hidden="true" />
        <div>
          <strong>Mục tiêu hôm nay</strong>
          <span>12/20 từ vựng</span>
        </div>
        <ProgressBar value={60} />
      </section>
    </aside>
  );
}
