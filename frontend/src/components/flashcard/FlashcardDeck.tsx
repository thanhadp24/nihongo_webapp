import { RotateCcw, Shuffle, Volume2 } from "lucide-react";
import { useCallback, useEffect, useMemo, useState } from "react";
import type { FlashcardItem } from "../../types/learning";
import { speakJapanese, speakJapaneseSequence } from "../../utils/speech";
import { Pagination } from "../common/Pagination";

export function FlashcardDeck({ items }: { items: FlashcardItem[] }) {
  const [index, setIndex] = useState(0);
  const [flipped, setFlipped] = useState(false);
  const [shuffleSeed, setShuffleSeed] = useState(0);

  const cards = useMemo(() => {
    if (shuffleSeed === 0) return items;

    const score = (value: string) =>
      [...`${shuffleSeed}-${value}`].reduce(
        (total, char) => (total * 31 + char.charCodeAt(0)) % 9973,
        17
      );

    return [...items].sort((a, b) => score(a.id) - score(b.id));
  }, [items, shuffleSeed]);

  const card = cards[index];
  const exampleAudioText = card?.exampleAudioText ?? card?.example ?? "";

  const goToCard = useCallback((nextIndex: number) => {
    setIndex(Math.min(Math.max(nextIndex, 0), Math.max(cards.length - 1, 0)));
    setFlipped(false);
  }, [cards.length]);

  useEffect(() => {
    if (index >= cards.length) goToCard(cards.length - 1);
  }, [cards.length, goToCard, index]);

  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      const target = event.target as HTMLElement | null;
      const isTyping =
        target?.tagName === "INPUT" ||
        target?.tagName === "TEXTAREA" ||
        target?.tagName === "SELECT" ||
        Boolean(target?.isContentEditable);

      if (isTyping) return;

      if (event.key === "ArrowRight" || event.key === "PageDown") {
        event.preventDefault();
        goToCard(index + 1);
      }

      if (event.key === "ArrowLeft" || event.key === "PageUp") {
        event.preventDefault();
        goToCard(index - 1);
      }
    };

    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [goToCard, index]);

  if (!card) return null;

  return (
    <section className="flashcard-stage">
      <div className="flashcard-toolbar">
        <span>{card.tag ?? "Flashcard"}</span>
        <div>
          <button
            className="secondary-button"
            onClick={() => speakJapaneseSequence([card.front, exampleAudioText])}
            type="button"
          >
            <Volume2 aria-hidden="true" />
            Nghe
          </button>
          {exampleAudioText ? (
            <button
              className="secondary-button"
              onClick={() => speakJapanese(exampleAudioText)}
              type="button"
            >
              <Volume2 aria-hidden="true" />
              Ví dụ
            </button>
          ) : null}
          <button
            className="secondary-button"
            onClick={() => {
              setShuffleSeed(Date.now());
              setIndex(0);
              setFlipped(false);
            }}
            type="button"
          >
            <Shuffle aria-hidden="true" />
            Trộn thẻ
          </button>
          <button
            className="secondary-button"
            onClick={() => setFlipped(false)}
            type="button"
          >
            <RotateCcw aria-hidden="true" />
            Lật lại
          </button>
        </div>
      </div>

      <button
        className={flipped ? "flashcard flipped" : "flashcard"}
        onClick={() => setFlipped((current) => !current)}
        type="button"
      >
        <span>{flipped ? "Mặt sau" : "Mặt trước"}</span>
        <strong>{flipped ? card.back : card.front}</strong>
        {flipped ? (
          <>
            {card.backSubtext ? <p>{card.backSubtext}</p> : null}
            {card.example ? <small>{card.example}</small> : null}
          </>
        ) : (
          card.frontSubtext ? <p>{card.frontSubtext}</p> : null
        )}
      </button>

      <Pagination
        onPageChange={(nextIndex) => {
          goToCard(nextIndex - 1);
        }}
        page={index + 1}
        pageSize={1}
        total={cards.length}
      />
    </section>
  );
}
