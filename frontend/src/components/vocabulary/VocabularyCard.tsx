import { Check, Heart, Volume2 } from "lucide-react";
import type { Vocabulary } from "../../types/learning";
import { StatusBadge } from "../common/StatusBadge";

export function VocabularyCard({ item }: { item: Vocabulary }) {
  return (
    <article className="vocabulary-card">
      <div className="vocab-actions">
        <button aria-label="Nghe phát âm" className="icon-button" type="button">
          <Volume2 aria-hidden="true" />
        </button>
        <button
          aria-label={item.saved ? "Bỏ lưu từ vựng" : "Lưu từ vựng"}
          className={item.saved ? "icon-button active" : "icon-button"}
          type="button"
        >
          <Heart aria-hidden="true" />
        </button>
        <button aria-label="Đánh dấu đã học" className="icon-button" type="button">
          <Check aria-hidden="true" />
        </button>
      </div>
      <div>
        <h2>{item.word}</h2>
        <p className="japanese-caption">{item.reading}</p>
        <p className="romaji">{item.romaji}</p>
      </div>
      <strong className="meaning">{item.meaning}</strong>
      <div className="card-title-row">
        <span className="soft-badge">{item.partOfSpeech}</span>
        <StatusBadge status={item.status} />
      </div>
      <div className="example-box">
        <span>Ví dụ</span>
        <p className="example-jp">{item.example}</p>
        <p>{item.exampleMeaning}</p>
      </div>
    </article>
  );
}
