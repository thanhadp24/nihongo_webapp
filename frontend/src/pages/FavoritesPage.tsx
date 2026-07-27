import { Heart, Trash2 } from "lucide-react";
import { Link } from "react-router";
import { PageHeader } from "../components/common/PageHeader";
import { EmptyState } from "../components/common/StateViews";
import { useSavedContent } from "../hooks/useSavedContent";
import { savedContentService } from "../services/savedContentService";

const typeLabel = {
  vocabulary: "Từ vựng",
  kanji: "Kanji"
};

export function FavoritesPage() {
  const items = useSavedContent();

  return (
    <div className="page-stack">
      <PageHeader
        eyebrow="Đã lưu"
        subtitle="Danh sách này lưu trên trình duyệt của bạn bằng localStorage."
        title="Nội dung đã lưu"
      />
      {items.length > 0 ? (
        <section className="saved-list">
          {items.map((item) => (
            <article className="saved-card" key={item.key}>
              <div className="saved-card-mark">
                <Heart aria-hidden="true" />
              </div>
              <div>
                <p className="eyebrow">{typeLabel[item.type]}</p>
                <h2>{item.title}</h2>
                {item.subtitle ? <p className="japanese-caption">{item.subtitle}</p> : null}
                <strong>{item.meaning}</strong>
                {item.detail ? <span>{item.detail}</span> : null}
              </div>
              <div className="saved-card-actions">
                <Link className="secondary-button" to={item.href}>
                  Mở lại
                </Link>
                <button
                  aria-label="Bỏ lưu"
                  className="icon-button"
                  onClick={() => savedContentService.remove(item.key)}
                  type="button"
                >
                  <Trash2 aria-hidden="true" />
                </button>
              </div>
            </article>
          ))}
        </section>
      ) : (
        <EmptyState
          text="Bấm biểu tượng trái tim ở từ vựng hoặc Kanji để lưu vào đây."
          title="Chưa có nội dung đã lưu"
        />
      )}
    </div>
  );
}
