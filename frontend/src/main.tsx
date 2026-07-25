import React, { useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

type Topic = {
  id: string;
  title: string;
  words: number;
  status: "new" | "learning" | "done";
};

type Chapter = {
  id: string;
  title: string;
  summary: string;
  topics: Topic[];
};

type JlptLevel = {
  code: string;
  name: string;
  caption: string;
  accent: string;
  chapters: Chapter[];
};

const jlptLevels: JlptLevel[] = [
  {
    code: "N5",
    name: "JLPT N5",
    caption: "Nen tang giao tiep",
    accent: "#2d7d78",
    chapters: [
      {
        id: "n5-c1",
        title: "Chapter 1: Chao hoi va gioi thieu",
        summary: "Cac mau cau va tu vung dung trong lan gap dau.",
        topics: [
          { id: "n5-c1-t1", title: "Chao hoi hang ngay", words: 24, status: "done" },
          { id: "n5-c1-t2", title: "Gioi thieu ban than", words: 31, status: "learning" },
          { id: "n5-c1-t3", title: "Quoc tich va nghe nghiep", words: 28, status: "new" }
        ]
      },
      {
        id: "n5-c2",
        title: "Chapter 2: Gia dinh va doi song",
        summary: "Tu vung co ban de noi ve nguoi than, nha cua, vat dung.",
        topics: [
          { id: "n5-c2-t1", title: "Thanh vien gia dinh", words: 36, status: "learning" },
          { id: "n5-c2-t2", title: "Do dung trong nha", words: 42, status: "new" },
          { id: "n5-c2-t3", title: "Bua an va thuc pham", words: 39, status: "new" }
        ]
      },
      {
        id: "n5-c3",
        title: "Chapter 3: Thoi gian va lich trinh",
        summary: "Ngay thang, gio giac, tan suat va cac hoat dong lap lai.",
        topics: [
          { id: "n5-c3-t1", title: "Ngay, thang, nam", words: 27, status: "done" },
          { id: "n5-c3-t2", title: "Lich sinh hoat", words: 34, status: "learning" },
          { id: "n5-c3-t3", title: "Di lai co ban", words: 30, status: "new" }
        ]
      }
    ]
  },
  {
    code: "N4",
    name: "JLPT N4",
    caption: "Mo rong van canh",
    accent: "#5f6fb7",
    chapters: [
      {
        id: "n4-c1",
        title: "Chapter 1: Cong viec va truong hoc",
        summary: "Cach noi ve nhiem vu, lich hoc, quy tac va ke hoach.",
        topics: [
          { id: "n4-c1-t1", title: "Van phong va cuoc hop", words: 45, status: "learning" },
          { id: "n4-c1-t2", title: "Mon hoc va bai tap", words: 40, status: "new" },
          { id: "n4-c1-t3", title: "Xin phep va de nghi", words: 33, status: "new" }
        ]
      },
      {
        id: "n4-c2",
        title: "Chapter 2: Mua sam va dich vu",
        summary: "Tinh huong tai cua hang, nha hang, nha ga va quay dich vu.",
        topics: [
          { id: "n4-c2-t1", title: "Gia ca va thanh toan", words: 37, status: "done" },
          { id: "n4-c2-t2", title: "Nha hang va dat mon", words: 41, status: "learning" },
          { id: "n4-c2-t3", title: "Hoi duong va ho tro", words: 35, status: "new" }
        ]
      }
    ]
  },
  {
    code: "N3",
    name: "JLPT N3",
    caption: "Doc hieu thuc te",
    accent: "#b6652f",
    chapters: [
      {
        id: "n3-c1",
        title: "Chapter 1: Xa hoi va tin tuc",
        summary: "Tu vung hay gap trong thong bao, bai doc ngan va tin tuc.",
        topics: [
          { id: "n3-c1-t1", title: "Thong bao cong cong", words: 48, status: "learning" },
          { id: "n3-c1-t2", title: "Tin tuc doi song", words: 52, status: "new" },
          { id: "n3-c1-t3", title: "YKien va danh gia", words: 44, status: "new" }
        ]
      },
      {
        id: "n3-c2",
        title: "Chapter 2: Cam xuc va quan he",
        summary: "Noi ve suy nghi, cam nhan, loi khuyen va mong doi.",
        topics: [
          { id: "n3-c2-t1", title: "Tinh cam ca nhan", words: 46, status: "done" },
          { id: "n3-c2-t2", title: "Quan he ban be", words: 43, status: "learning" },
          { id: "n3-c2-t3", title: "Loi khuyen va canh bao", words: 49, status: "new" }
        ]
      }
    ]
  },
  {
    code: "N2",
    name: "JLPT N2",
    caption: "Tu duy hoc thuat",
    accent: "#8b5c9f",
    chapters: [
      {
        id: "n2-c1",
        title: "Chapter 1: Kinh te va cong viec",
        summary: "Cum tu chuyen sau cho moi truong lam viec va bai doc dai.",
        topics: [
          { id: "n2-c1-t1", title: "Tuyen dung va hop dong", words: 58, status: "learning" },
          { id: "n2-c1-t2", title: "Ke hoach kinh doanh", words: 61, status: "new" },
          { id: "n2-c1-t3", title: "Bao cao va phan tich", words: 54, status: "new" }
        ]
      },
      {
        id: "n2-c2",
        title: "Chapter 2: Van hoa va truyen thong",
        summary: "Tu vung ve phong tuc, quan diem xa hoi va bai luan ngan.",
        topics: [
          { id: "n2-c2-t1", title: "Le hoi va nghi thuc", words: 55, status: "done" },
          { id: "n2-c2-t2", title: "Nghe thuat dai chung", words: 50, status: "new" },
          { id: "n2-c2-t3", title: "Gia tri xa hoi", words: 57, status: "new" }
        ]
      }
    ]
  },
  {
    code: "N1",
    name: "JLPT N1",
    caption: "Ngon ngu chuyen sau",
    accent: "#a64d58",
    chapters: [
      {
        id: "n1-c1",
        title: "Chapter 1: Binh luan va nghien cuu",
        summary: "Tu vung truu tuong trong bai doc hoc thuat va xa luan.",
        topics: [
          { id: "n1-c1-t1", title: "Lap luan va phan bien", words: 66, status: "learning" },
          { id: "n1-c1-t2", title: "Nghien cuu va so lieu", words: 72, status: "new" },
          { id: "n1-c1-t3", title: "Xa luan chuyen sau", words: 68, status: "new" }
        ]
      },
      {
        id: "n1-c2",
        title: "Chapter 2: Van phong nang cao",
        summary: "Ngon ngu trang trong cho thu tin, dam phan va bao cao.",
        topics: [
          { id: "n1-c2-t1", title: "Thu tin trang trong", words: 60, status: "done" },
          { id: "n1-c2-t2", title: "Dam phan va dieu chinh", words: 65, status: "learning" },
          { id: "n1-c2-t3", title: "Bao cao cap quan ly", words: 63, status: "new" }
        ]
      }
    ]
  }
];

const statusLabels: Record<Topic["status"], string> = {
  done: "Da hoc",
  learning: "Dang hoc",
  new: "Moi"
};

function App() {
  const [selectedLevelCode, setSelectedLevelCode] = useState(jlptLevels[0].code);
  const [isLoading, setIsLoading] = useState(false);

  const selectedLevel = useMemo(
    () => jlptLevels.find((level) => level.code === selectedLevelCode) ?? jlptLevels[0],
    [selectedLevelCode]
  );

  useEffect(() => {
    setIsLoading(true);
    const timeoutId = window.setTimeout(() => setIsLoading(false), 260);

    return () => window.clearTimeout(timeoutId);
  }, [selectedLevelCode]);

  const totalTopics = selectedLevel.chapters.reduce(
    (count, chapter) => count + chapter.topics.length,
    0
  );

  return (
    <main className="app-shell">
      <section className="workspace">
        <aside className="level-panel" aria-label="Danh sach cap do JLPT">
          <div className="brand-block">
            <span className="brand-mark">日</span>
            <div>
              <p className="eyebrow">Nihongo Webapp</p>
              <h1>JLPT Study Map</h1>
            </div>
          </div>

          <div className="level-list" role="list">
            {jlptLevels.map((level) => {
              const isActive = selectedLevel.code === level.code;

              return (
                <button
                  className={`level-button${isActive ? " active" : ""}`}
                  key={level.code}
                  onClick={() => setSelectedLevelCode(level.code)}
                  style={{ "--level-accent": level.accent } as React.CSSProperties}
                  type="button"
                >
                  <span className="level-code">{level.code}</span>
                  <span className="level-copy">
                    <strong>{level.name}</strong>
                    <small>{level.caption}</small>
                  </span>
                </button>
              );
            })}
          </div>
        </aside>

        <section className="content-panel" aria-live="polite">
          <header className="content-header">
            <div>
              <p className="eyebrow">Lo trinh dang chon</p>
              <h2>{selectedLevel.name}</h2>
            </div>
            <dl className="level-stats">
              <div>
                <dt>Chapter</dt>
                <dd>{selectedLevel.chapters.length}</dd>
              </div>
              <div>
                <dt>Chu de</dt>
                <dd>{totalTopics}</dd>
              </div>
            </dl>
          </header>

          {isLoading ? (
            <div className="loading-state">
              <span className="loader" />
              <span>Dang tai chapter...</span>
            </div>
          ) : (
            <div className="chapter-list">
              {selectedLevel.chapters.map((chapter, index) => (
                <article className="chapter-card" key={chapter.id}>
                  <div className="chapter-index">{String(index + 1).padStart(2, "0")}</div>
                  <div className="chapter-body">
                    <div className="chapter-heading">
                      <div>
                        <h3>{chapter.title}</h3>
                        <p>{chapter.summary}</p>
                      </div>
                      <span>{chapter.topics.length} chu de</span>
                    </div>

                    <div className="topic-grid">
                      {chapter.topics.map((topic) => (
                        <button className="topic-item" key={topic.id} type="button">
                          <span className={`topic-status ${topic.status}`}>
                            {statusLabels[topic.status]}
                          </span>
                          <strong>{topic.title}</strong>
                          <small>{topic.words} tu vung</small>
                        </button>
                      ))}
                    </div>
                  </div>
                </article>
              ))}
            </div>
          )}
        </section>
      </section>
    </main>
  );
}

createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
