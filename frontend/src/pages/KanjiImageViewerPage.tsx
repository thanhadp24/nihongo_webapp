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
import { Link, useParams } from "react-router";
import { api } from "../api";
import { Breadcrumb } from "../components/common/Breadcrumb";
import { EmptyState, ErrorState, SkeletonCard } from "../components/common/StateViews";
import { PageHeader } from "../components/common/PageHeader";

const minZoom = 0.6;
const maxZoom = 3;
const zoomStep = 0.2;

function imageDisplayUrl(url: string) {
  if (url.startsWith("https://drive.google.com/thumbnail?") && !url.includes("&sz=")) {
    return `${url}&sz=w2200`;
  }

  return url;
}

function clamp(value: number, min: number, max: number) {
  return Math.min(Math.max(value, min), max);
}

export function KanjiImageViewerPage() {
  const { levelId = "n5" } = useParams();
  const [index, setIndex] = useState(0);
  const [zoom, setZoom] = useState(1);

  const resourcesQuery = useQuery({
    queryKey: ["visual-resources", "kanji", levelId],
    queryFn: () => api.visualResources({ category: "kanji", level: levelId }),
    enabled: Boolean(levelId)
  });

  const resources = resourcesQuery.data ?? [];
  const current = resources[index];
  const imageUrl = useMemo(() => (current ? imageDisplayUrl(current.image_url) : ""), [current]);
  const canGoPrevious = index > 0;
  const canGoNext = index < resources.length - 1;

  useEffect(() => {
    setIndex(0);
    setZoom(1);
  }, [levelId]);

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

  return (
    <div className="page-stack">
      <Breadcrumb
        items={[
          { label: "Trang chủ", to: "/" },
          { label: levelId.toUpperCase(), to: `/jlpt/${levelId}` },
          { label: "Kanji", to: `/jlpt/${levelId}/kanji` },
          { label: "Ảnh Kanji" }
        ]}
      />

      <PageHeader
        actions={
          <Link className="secondary-button" to={`/jlpt/${levelId}/kanji`}>
            <ChevronLeft aria-hidden="true" />
            Kanji
          </Link>
        }
        eyebrow={levelId.toUpperCase()}
        subtitle="Xem bộ ảnh Kanji theo đúng thứ tự dữ liệu đã import."
        title="Ảnh Kanji"
      />

      {resourcesQuery.isLoading ? <SkeletonCard count={3} /> : null}
      {resourcesQuery.isError ? <ErrorState onRetry={() => resourcesQuery.refetch()} /> : null}

      {!resourcesQuery.isLoading && !resourcesQuery.isError && resources.length === 0 ? (
        <EmptyState text="Level này chưa có ảnh Kanji." title="Chưa có ảnh" />
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
              <p className="eyebrow">{current.jlpt_level_code}</p>
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

          <div className="kanji-image-strip" aria-label="Danh sách ảnh Kanji">
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
