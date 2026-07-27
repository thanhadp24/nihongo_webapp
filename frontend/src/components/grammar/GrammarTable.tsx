import { BookOpen, CheckCircle2, Volume2 } from "lucide-react";
import { Link } from "react-router";
import type { Lesson } from "../../types/learning";
import { speakJapanese } from "../../utils/speech";

function compactText(value?: string, fallback = "Chưa có dữ liệu") {
  if (!value?.trim()) return fallback;
  return value;
}

export function GrammarTable({ lessons }: { lessons: Lesson[] }) {
  return (
    <div className="grammar-table-wrap">
      <table className="grammar-table">
        <thead>
          <tr>
            <th>Mẫu ngữ pháp</th>
            <th>Nghĩa</th>
            <th>Cấu trúc</th>
            <th>Giải thích</th>
            <th>Ví dụ</th>
            <th>Ôn tập</th>
          </tr>
        </thead>
        <tbody>
          {lessons.map((lesson) => (
            <tr key={lesson.id}>
              <td>
                <div className="grammar-pattern-cell">
                  <button
                    aria-label="Nghe mẫu ngữ pháp"
                    className="icon-button"
                    onClick={() => speakJapanese(lesson.japaneseTitle)}
                    type="button"
                  >
                    <Volume2 aria-hidden="true" />
                  </button>
                  <div>
                    <strong>{lesson.japaneseTitle}</strong>
                    <span>{lesson.title}</span>
                  </div>
                </div>
              </td>
              <td>{compactText(lesson.meaning || lesson.title)}</td>
              <td>{compactText(lesson.formation || lesson.japaneseTitle)}</td>
              <td>
                <p className="table-clamp">{compactText(lesson.explanation)}</p>
              </td>
              <td>
                {lesson.example ? (
                  <div className="grammar-example-cell">
                    <button
                      aria-label="Nghe ví dụ"
                      className="icon-button"
                      onClick={() => speakJapanese(lesson.example ?? "")}
                      type="button"
                    >
                      <Volume2 aria-hidden="true" />
                    </button>
                    <div>
                      <strong>{lesson.example}</strong>
                      {lesson.exampleMeaning ? <span>{lesson.exampleMeaning}</span> : null}
                    </div>
                  </div>
                ) : (
                  "Chưa có ví dụ"
                )}
              </td>
              <td>
                <Link className="secondary-button table-action" to={`/lessons/${lesson.id}`}>
                  <BookOpen aria-hidden="true" />
                  Chi tiết
                </Link>
                <button className="primary-button table-action" type="button">
                  <CheckCircle2 aria-hidden="true" />
                  Ôn
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
