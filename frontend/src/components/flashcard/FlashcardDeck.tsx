import { RotateCcw, Shuffle } from "lucide-react";
import { useMemo, useState } from "react";
import type { FlashcardItem } from "../../types/learning";
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

  if (!card) return null;

  return (
    <section className="flashcard-stage">
      <div className="flashcard-toolbar">
        <span>{card.tag ?? "Flashcard"}</span>
        <div>
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
          setIndex(nextIndex - 1);
          setFlipped(false);
        }}
        page={index + 1}
        pageSize={1}
        total={cards.length}
      />
    </section>
  );
}
