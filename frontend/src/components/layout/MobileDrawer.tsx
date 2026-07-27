import { X } from "lucide-react";
import type { ReactNode } from "react";

export function MobileDrawer({
  children,
  onClose,
  open
}: {
  children: ReactNode;
  onClose: () => void;
  open: boolean;
}) {
  if (!open) return null;

  return (
    <div className="drawer-overlay" onClick={onClose}>
      <aside className="mobile-drawer" onClick={(event) => event.stopPropagation()}>
        <div className="drawer-title-row">
          <strong>Menu</strong>
          <button aria-label="Đóng menu" className="icon-button" onClick={onClose} type="button">
            <X aria-hidden="true" />
          </button>
        </div>
        {children}
      </aside>
    </div>
  );
}
