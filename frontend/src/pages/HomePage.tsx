import { ArrowRight, Play } from "lucide-react";
import { Link } from "react-router";
import { JLPTLevelCard } from "../components/jlpt/JLPTLevelCard";
import { PageHeader } from "../components/common/PageHeader";
import { learningService } from "../services/learningService";

export function HomePage() {
  const levels = learningService.getLevels();
  const continueLesson = learningService.getContinueLesson();

  return (
    <div className="page-stack">
      <section className="hero-panel">
        <div>
          <p className="eyebrow">Tiếp tục hành trình học tập</p>
          <h1>Bạn đang học JLPT N5 - Chapter 1</h1>
          <p>Nội dung nổi bật hôm nay: chào hỏi, giới thiệu bản thân và ôn lại từ cần nhớ.</p>
        </div>
        <div className="hero-progress">
          <span>Tiến độ hiện tại</span>
          <strong>62%</strong>
          <Link className="primary-button" to="/jlpt/n5/chapters/n5-c1/topics/n5-c1-t1">
            <Play aria-hidden="true" />
            Tiếp tục học
          </Link>
        </div>
      </section>

      <section className="recent-card">
        <div>
          <p className="eyebrow">Bài gần nhất</p>
          <h2>{continueLesson?.title ?? "Chưa có bài học gần nhất"}</h2>
          <p>{continueLesson?.japaneseTitle ?? "Hãy chọn một cấp độ để bắt đầu."}</p>
        </div>
        {continueLesson ? (
          <Link className="secondary-button" to={`/lessons/${continueLesson.id}`}>
            Mở bài học
            <ArrowRight aria-hidden="true" />
          </Link>
        ) : null}
      </section>

      <PageHeader
        title="Lộ trình học JLPT"
        subtitle="Chọn cấp độ phù hợp để bắt đầu học tiếng Nhật."
      />
      <section className="level-grid">
        {levels.map((level) => (
          <JLPTLevelCard key={level.id} level={level} />
        ))}
      </section>
    </div>
  );
}
