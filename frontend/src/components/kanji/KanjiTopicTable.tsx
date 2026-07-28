import { useEffect, useMemo, useState } from "react";
import { BookOpen } from "lucide-react";
import type { KanjiTopicSummary } from "../../types/learning";
import { Pagination } from "../common/Pagination";

function weekLabel(topic: KanjiTopicSummary) {
  if (topic.sourceWeek) return `Tuần ${topic.sourceWeek}`;
  return "Chưa phân tuần";
}

function weekOrder(label: string) {
  const value = Number(label.replace(/\D/g, ""));
  return Number.isFinite(value) && value > 0 ? value : Number.MAX_SAFE_INTEGER;
}

export function KanjiTopicTable({
  levelId,
  onSelect,
  topics
}: {
  levelId: string;
  onSelect: (topicId: string) => void;
  topics: KanjiTopicSummary[];
}) {
  const [page, setPage] = useState(1);
  const groups = useMemo(() => {
    const grouped = topics.reduce<Record<string, KanjiTopicSummary[]>>((result, topic) => {
      const key = weekLabel(topic);
      result[key] = [...(result[key] ?? []), topic];
      return result;
    }, {});

    return Object.entries(grouped).sort(([left], [right]) => weekOrder(left) - weekOrder(right));
  }, [topics]);
  const currentGroup = groups[page - 1];
  const [week, items] = currentGroup ?? ["", []];

  useEffect(() => {
    setPage(1);
  }, [topics]);

  if (!currentGroup) return null;

  return (
    <div className="kanji-week-stack">
      <section className="kanji-week-panel">
        <div className="card-title-row">
          <div>
            <p className="eyebrow">{week}</p>
            <h2>{items.reduce((total, topic) => total + topic.characterCount, 0)} Kanji</h2>
          </div>
        </div>
        <div className="kanji-topic-table-wrap">
          <table className="kanji-topic-table">
            <thead>
              <tr>
                <th>Ngày</th>
                <th>Chủ đề</th>
                <th>Nghĩa</th>
                <th>Số Kanji</th>
                <th>Ôn tập</th>
              </tr>
            </thead>
            <tbody>
              {items.map((topic) => (
                <tr key={topic.id}>
                  <td>{topic.sourceDay ? `Ngày ${topic.sourceDay}` : "-"}</td>
                  <td>
                    <strong>{topic.title}</strong>
                    {topic.reading ? <span>{topic.reading}</span> : null}
                  </td>
                  <td>{topic.meaning || topic.description || "-"}</td>
                  <td>{topic.characterCount}</td>
                  <td>
                    <button className="secondary-button table-action" onClick={() => onSelect(topic.id)} type="button">
                      <BookOpen aria-hidden="true" />
                      Xem Kanji
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
      <Pagination onPageChange={setPage} page={page} pageSize={1} total={groups.length} />
    </div>
  );
}
