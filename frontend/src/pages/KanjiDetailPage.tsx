import { useQuery } from "@tanstack/react-query";
import { ArrowLeft, Heart, Volume2 } from "lucide-react";
import { Link, Navigate, useLocation, useParams } from "react-router";
import { PageHeader } from "../components/common/PageHeader";
import { ErrorState, SkeletonCard } from "../components/common/StateViews";
import { useSavedState } from "../hooks/useSavedContent";
import { apiLearningService } from "../services/apiLearningService";
import { savedContentService } from "../services/savedContentService";
import { speakJapanese } from "../utils/speech";

export function KanjiDetailPage() {
  const { kanjiId = "" } = useParams();
  const location = useLocation();
  const backHref = (location.state as { from?: string } | null)?.from ?? "/jlpt/n2/kanji";
  const saved = useSavedState("kanji", kanjiId);
  const kanjiQuery = useQuery({
    queryKey: ["learning-kanji-detail", kanjiId],
    queryFn: () => apiLearningService.getKanjiDetail(kanjiId),
    enabled: Boolean(kanjiId)
  });

  if (kanjiQuery.data && !kanjiQuery.data.kanji) return <Navigate to="/jlpt" replace />;

  const kanji = kanjiQuery.data?.kanji;
  const detail = kanjiQuery.data?.detail;
  const words = detail?.words ?? [];

  return (
    <div className="page-stack">
      {kanjiQuery.isLoading ? <SkeletonCard count={2} /> : null}
      {kanjiQuery.isError ? <ErrorState onRetry={() => kanjiQuery.refetch()} /> : null}
      {kanji ? (
        <>
          <PageHeader
            actions={
              <>
                <button
                  className="secondary-button"
                  onClick={() => speakJapanese(kanji.character)}
                  type="button"
                >
                  <Volume2 aria-hidden="true" />
                  Nghe
                </button>
                <button
                  className={saved ? "primary-button" : "secondary-button"}
                  onClick={() =>
                    savedContentService.toggle({
                      type: "kanji",
                      id: kanji.id,
                      title: kanji.character,
                      subtitle: [kanji.onyomi, kanji.kunyomi].filter(Boolean).join(" / "),
                      meaning: kanji.meaning,
                      detail: kanji.hanViet ? `Hán Việt: ${kanji.hanViet}` : kanji.topicMeaning,
                      href: `/kanji/${kanji.id}`
                    })
                  }
                  type="button"
                >
                  <Heart aria-hidden="true" />
                  {saved ? "Đã lưu" : "Lưu"}
                </button>
              </>
            }
            eyebrow={kanji.topicMeaning || kanji.topicName}
            subtitle={kanji.hanViet ? `Hán Việt: ${kanji.hanViet}` : undefined}
            title={kanji.character}
          />

          <section className="kanji-detail-panel">
            <div className="kanji-detail-symbol">{kanji.character}</div>
            <div className="grammar-detail-table-wrap">
              <table className="grammar-detail-table">
                <tbody>
                  <tr>
                    <th>Nghĩa</th>
                    <td>{kanji.meaning}</td>
                  </tr>
                  <tr>
                    <th>Onyomi</th>
                    <td>{kanji.onyomi || "Chưa có dữ liệu"}</td>
                  </tr>
                  <tr>
                    <th>Kunyomi</th>
                    <td>{kanji.kunyomi || "Chưa có dữ liệu"}</td>
                  </tr>
                  <tr>
                    <th>Số nét</th>
                    <td>{kanji.strokeCount ?? "Chưa có dữ liệu"}</td>
                  </tr>
                  <tr>
                    <th>Gợi nhớ</th>
                    <td>{kanji.mnemonic || "Chưa có dữ liệu gợi nhớ."}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </section>

          {words.length > 0 ? (
            <section className="grammar-examples-panel">
              <div>
                <p className="eyebrow">Từ ghép</p>
                <h2>Ví dụ dùng Kanji</h2>
              </div>
              <div className="kanji-word-list">
                {words.map((word) => (
                  <article className="kanji-word-row" key={word.id}>
                    <button
                      aria-label="Nghe từ ghép"
                      className="icon-button"
                      onClick={() => speakJapanese(word.word)}
                      type="button"
                    >
                      <Volume2 aria-hidden="true" />
                    </button>
                    <div>
                      <strong>{word.word}</strong>
                      {word.reading ? <span>{word.reading}</span> : null}
                    </div>
                    <p>{word.meaning_vi}</p>
                  </article>
                ))}
              </div>
            </section>
          ) : null}

          <Link className="secondary-button back-button" to={backHref}>
            <ArrowLeft aria-hidden="true" />
            Quay lại
          </Link>
        </>
      ) : null}
    </div>
  );
}
