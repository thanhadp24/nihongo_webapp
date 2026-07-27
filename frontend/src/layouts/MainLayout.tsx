import { useState } from "react";
import { Outlet } from "react-router";
import { AppHeader } from "../components/layout/AppHeader";
import { DesktopSidebar } from "../components/layout/DesktopSidebar";
import { MobileBottomNavigation } from "../components/layout/MobileBottomNavigation";
import { MobileDrawer } from "../components/layout/MobileDrawer";

export function MainLayout() {
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);

  return (
    <div className="app-shell">
      <AppHeader onMenuClick={() => setIsDrawerOpen(true)} />
      <div className="app-grid">
        <DesktopSidebar />
        <main className="content-shell">
          <Outlet />
        </main>
      </div>
      <MobileDrawer open={isDrawerOpen} onClose={() => setIsDrawerOpen(false)}>
        <DesktopSidebar compact />
      </MobileDrawer>
      <MobileBottomNavigation />
    </div>
  );
}
