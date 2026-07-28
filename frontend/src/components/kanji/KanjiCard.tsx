import { BookMarked, Heart, Volume2 } from "lucide-react";
import { Link, useLocation } from "react-router";
import { useSavedState } from "../../hooks/useSavedContent";
import { savedContentService } from "../../services/savedContentService";
import type { Kanji } from "../../types/learning";
import { speakJapanese } from "../../utils/speech";

export function KanjiCard({ detailHref, item }: { detailHref?: string; item: Kanji }) {
  const { pathname } = useLocation();
  const saved = useSavedState("kanji", item.id);
  const href = detailHref ?? `/kanji/${item.id}`;

  return (
    <article className="kanji-card">
      <div className="vocab-actions">
        <button
          aria-label="Nghe Kanji"
          className="icon-button"
          onClick={() => speakJapanese(item.character)}
          type="button"
        >
          <Volume2 aria-hidden="true" />
        </button>
        <button
          aria-label={saved ? "Bỏ lưu Kanji" : "Lưu Kanji"}
          className={saved ? "icon-button active" : "icon-button"}
          onClick={() =>
            savedContentService.toggle({
              type: "kanji",
              id: item.id,
              title: item.character,
              subtitle: [item.onyomi, item.kunyomi].filter(Boolean).join(" / "),
              meaning: item.meaning,
              detail: item.hanViet ? `Hán Việt: ${item.hanViet}` : item.topicMeaning,
              href
            })
          }
          type="button"
        >
          <Heart aria-hidden="true" />
        </button>
        <Link aria-label="Xem chi tiết Kanji" className="icon-button" state={{ from: pathname }} to={href}>
          <BookMarked aria-hidden="true" />
        </Link>
      </div>
      <div className="kanji-symbol">{item.character}</div>
      <div>
        <strong className="meaning">{item.meaning}</strong>
        {item.hanViet ? <p className="romaji">Hán Việt: {item.hanViet}</p> : null}
      </div>
      <div className="stat-row">
        {item.onyomi ? <span>On: {item.onyomi}</span> : null}
        {item.kunyomi ? <span>Kun: {item.kunyomi}</span> : null}
        {item.strokeCount ? <span>{item.strokeCount} nét</span> : null}
      </div>
      <div className="card-title-row">
        <span className="soft-badge">{item.topicMeaning || item.topicName}</span>
      </div>
      {item.mnemonic ? (
        <div className="example-box">
          <span>Gợi nhớ</span>
          <p>{item.mnemonic}</p>
        </div>
      ) : null}
    </article>
  );
}
