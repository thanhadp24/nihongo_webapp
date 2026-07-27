import { Bookmark, Home, Repeat, Route, UserRound } from "lucide-react";
import { NavLink } from "react-router";

const bottomItems = [
  { to: "/", label: "Trang chủ", icon: Home },
  { to: "/jlpt", label: "Lộ trình", icon: Route },
  { to: "/review", label: "Ôn tập", icon: Repeat },
  { to: "/favorites", label: "Đã lưu", icon: Bookmark },
  { to: "/profile", label: "Tài khoản", icon: UserRound }
];

export function MobileBottomNavigation() {
  return (
    <nav className="mobile-bottom-nav" aria-label="Điều hướng mobile">
      {bottomItems.map((item) => {
        const Icon = item.icon;
        return (
          <NavLink key={item.to} to={item.to}>
            <Icon aria-hidden="true" />
            <span>{item.label}</span>
          </NavLink>
        );
      })}
    </nav>
  );
}
