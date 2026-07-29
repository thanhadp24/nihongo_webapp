import { useCallback, useEffect, useMemo, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import {
  ChevronLeft,
  ChevronRight,
  Image as ImageIcon,
  RotateCcw,
  ZoomIn,
  ZoomOut
} from "lucide-react";
import { Navigate, useParams } from "react-router";
import { api } from "../api";
import { Breadcrumb } from "../components/common/Breadcrumb";
import { EmptyState, ErrorState, SkeletonCard } from "../components/common/StateViews";
import { PageHeader } from "../components/common/PageHeader";

const minZoom = 0.6;
const maxZoom = 3;
const zoomStep = 0.2;

type ViewerMode = "kanji" | "letters";

const viewerCopy: Record<
  ViewerMode,
  {
    breadcrumb: string;
    category: "kanji" | "reading";
    empty: string;
    subtitle: string;
    title: string;
  }
> = {
  kanji: {
    breadcrumb: "Theo Kanji",
    category: "kanji",
    empty: "Level này chưa có ảnh Kanji.",
    subtitle: "Xem bộ ảnh Kanji theo đúng thứ tự dữ liệu đã import.",
    title: "Học theo Kanji"
  },
  letters: {
    breadcrumb: "Theo lá thư",
    category: "reading",
    empty: "Chưa có ảnh lá thư đọc hiểu.",
    subtitle: "Xem các lá thư đọc hiểu theo đúng thứ tự file đã import.",
    title: "Học theo lá thư"
  }
};

function imageDisplayUrl(url: string) {
  if (url.startsWith("https://drive.google.com/thumbnail?") && !url.includes("&sz=")) {
    return `${url}&sz=w2200`;
  }

  return url;
}

function clamp(value: number, min: number, max: number) {
  return Math.min(Math.max(value, min), max);
}

export function VisualResourceViewerPage() {
  const { levelId = "n5", mode = "kanji" } = useParams();
  const viewerMode = mode as ViewerMode;
  const isKnownMode = viewerMode in viewerCopy;
  const config = isKnownMode ? viewerCopy[viewerMode] : viewerCopy.kanji;
  const [index, setIndex] = useState(0);
  const [zoom, setZoom] = useState(1);

  const resourcesQuery = useQuery({
    queryKey: ["visual-resources", config?.category, viewerMode === "kanji" ? levelId : "all"],
    queryFn: () =>
      api.visualResources({
        category: config.category,
        level: viewerMode === "kanji" ? levelId : undefined
      }),
    enabled: isKnownMode
  });

  const resources = resourcesQuery.data ?? [];
  const current = resources[index];
  const imageUrl = useMemo(() => (current ? imageDisplayUrl(current.image_url) : ""), [current]);
  const canGoPrevious = index > 0;
  const canGoNext = index < resources.length - 1;

  useEffect(() => {
    setIndex(0);
    setZoom(1);
  }, [levelId, viewerMode]);

  useEffect(() => {
    if (index >= resources.length) {
      setIndex(Math.max(resources.length - 1, 0));
    }
  }, [index, resources.length]);

  const goToImage = useCallback(
    (nextIndex: number) => {
      setIndex(clamp(nextIndex, 0, Math.max(resources.length - 1, 0)));
      setZoom(1);
    },
    [resources.length]
  );

  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === "ArrowLeft" && canGoPrevious) {
        event.preventDefault();
        goToImage(index - 1);
      }
      if (event.key === "ArrowRight" && canGoNext) {
        event.preventDefault();
        goToImage(index + 1);
      }
      if ((event.key === "+" || event.key === "=") && current) {
        event.preventDefault();
        setZoom((value) => clamp(Number((value + zoomStep).toFixed(2)), minZoom, maxZoom));
      }
      if (event.key === "-" && current) {
        event.preventDefault();
        setZoom((value) => clamp(Number((value - zoomStep).toFixed(2)), minZoom, maxZoom));
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [canGoNext, canGoPrevious, current, goToImage, index]);

  if (!isKnownMode) return <Navigate to="/visual/kanji/n5" replace />;

  return (
    <div className="page-stack">
      <Breadcrumb
        items={[
          { label: "Trang chủ", to: "/" },
          { label: "Học bằng hình ảnh" },
          ...(viewerMode === "kanji" ? [{ label: levelId.toUpperCase() }] : []),
          { label: config.breadcrumb }
        ]}
      />

      <PageHeader
        eyebrow={viewerMode === "kanji" ? levelId.toUpperCase() : "Đọc hiểu"}
        subtitle={config.subtitle}
        title={config.title}
      />

      {resourcesQuery.isLoading ? <SkeletonCard count={3} /> : null}
      {resourcesQuery.isError ? <ErrorState onRetry={() => resourcesQuery.refetch()} /> : null}

      {!resourcesQuery.isLoading && !resourcesQuery.isError && resources.length === 0 ? (
        <EmptyState text={config.empty} title="Chưa có ảnh" />
      ) : null}

      {current ? (
        <section className="kanji-image-viewer">
          <div className="kanji-image-toolbar">
            <button
              aria-label="Ảnh trước"
              className="icon-button"
              disabled={!canGoPrevious}
              onClick={() => goToImage(index - 1)}
              title="Ảnh trước"
              type="button"
            >
              <ChevronLeft aria-hidden="true" />
            </button>
            <span>
              {index + 1} / {resources.length}
            </span>
            <button
              aria-label="Ảnh tiếp theo"
              className="icon-button"
              disabled={!canGoNext}
              onClick={() => goToImage(index + 1)}
              title="Ảnh tiếp theo"
              type="button"
            >
              <ChevronRight aria-hidden="true" />
            </button>
            <div className="kanji-image-toolbar-divider" />
            <button
              aria-label="Thu nhỏ"
              className="icon-button"
              disabled={zoom <= minZoom}
              onClick={() => setZoom((value) => clamp(Number((value - zoomStep).toFixed(2)), minZoom, maxZoom))}
              title="Thu nhỏ"
              type="button"
            >
              <ZoomOut aria-hidden="true" />
            </button>
            <strong>{Math.round(zoom * 100)}%</strong>
            <button
              aria-label="Phóng to"
              className="icon-button"
              disabled={zoom >= maxZoom}
              onClick={() => setZoom((value) => clamp(Number((value + zoomStep).toFixed(2)), minZoom, maxZoom))}
              title="Phóng to"
              type="button"
            >
              <ZoomIn aria-hidden="true" />
            </button>
            <button
              aria-label="Đặt lại zoom"
              className="icon-button"
              onClick={() => setZoom(1)}
              title="Đặt lại zoom"
              type="button"
            >
              <RotateCcw aria-hidden="true" />
            </button>
          </div>

          <div className="kanji-image-title-row">
            <div>
              <p className="eyebrow">
                {current.jlpt_level_code ?? (viewerMode === "letters" ? "Đọc hiểu" : config.title)}
              </p>
              <h2>{current.title}</h2>
            </div>
            <ImageIcon aria-hidden="true" />
          </div>

          <div className="kanji-image-stage">
            <div className="kanji-image-scroll">
              <img
                alt={current.title}
                key={current.id}
                loading="eager"
                src={imageUrl}
                style={{ width: `${zoom * 100}%` }}
              />
            </div>
          </div>

          <div className="kanji-image-strip" aria-label="Danh sách ảnh">
            {resources.map((resource, resourceIndex) => (
              <button
                aria-label={resource.title}
                aria-current={resourceIndex === index ? "true" : undefined}
                className={resourceIndex === index ? "active" : ""}
                key={resource.id}
                onClick={() => goToImage(resourceIndex)}
                type="button"
              >
                {resource.display_order}
              </button>
            ))}
          </div>
        </section>
      ) : null}
    </div>
  );
}
