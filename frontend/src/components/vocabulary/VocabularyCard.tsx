import { Check, Heart, Volume2 } from "lucide-react";
import { useLocation } from "react-router";
import { useSavedState } from "../../hooks/useSavedContent";
import { savedContentService } from "../../services/savedContentService";
import type { Vocabulary } from "../../types/learning";
import { speakJapanese, speakJapaneseSequence } from "../../utils/speech";

export function VocabularyCard({ item }: { item: Vocabulary }) {
  const { pathname } = useLocation();
  const saved = useSavedState("vocabulary", item.id);

  return (
    <article className="vocabulary-card">
      <div className="vocab-actions">
        <button
          aria-label="Nghe phát âm"
          className="icon-button"
          onClick={() => speakJapaneseSequence([item.word, item.example])}
          type="button"
        >
          <Volume2 aria-hidden="true" />
        </button>
        <button
          aria-label={saved ? "Bỏ lưu từ vựng" : "Lưu từ vựng"}
          className={saved ? "icon-button active" : "icon-button"}
          onClick={() =>
            savedContentService.toggle({
              type: "vocabulary",
              id: item.id,
              title: item.word,
              subtitle: item.reading,
              meaning: item.meaning,
              detail: item.partOfSpeech,
              href: pathname
            })
          }
          type="button"
        >
          <Heart aria-hidden="true" />
        </button>
        {/* <button aria-label="Đánh dấu đã học" className="icon-button" type="button">
          <Check aria-hidden="true" />
        </button> */}
      </div>
      <div>
        <h2>{item.word}</h2>
        <p className="japanese-caption">{item.reading}</p>
        {
          item.romaji === item.reading ? null : <p className="romaji">{item.romaji}</p>
        }
        {/* <p className="romaji">{item.romaji}</p> */}
      </div>
      <strong className="meaning">{item.meaning}</strong>
      <div className="card-title-row">
        <span className="soft-badge">{item.partOfSpeech}</span>
      </div>
      {item.example ? (
        <div className="example-box">
          <div className="example-box-title">
            <span>Ví dụ</span>
            <button
              aria-label="Nghe ví dụ"
              className="icon-button"
              onClick={() => speakJapanese(item.example)}
              type="button"
            >
              <Volume2 aria-hidden="true" />
            </button>
          </div>
          <p className="example-jp">{item.example}</p>
          <p>{item.exampleMeaning}</p>
        </div>
      ) : null}
    </article>
  );
}
