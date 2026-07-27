import { BookMarked, Heart, Volume2 } from "lucide-react";
import type { Kanji } from "../../types/learning";
import { speakJapanese } from "../../utils/speech";
import { StatusBadge } from "../common/StatusBadge";

export function KanjiCard({ item }: { item: Kanji }) {
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
          aria-label={item.saved ? "Bỏ lưu Kanji" : "Lưu Kanji"}
          className={item.saved ? "icon-button active" : "icon-button"}
          type="button"
        >
          <Heart aria-hidden="true" />
        </button>
        <button aria-label="Xem từ ghép" className="icon-button" type="button">
          <BookMarked aria-hidden="true" />
        </button>
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
        <StatusBadge status={item.status} />
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
