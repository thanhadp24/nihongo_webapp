import { JLPTLevelCard } from "../components/jlpt/JLPTLevelCard";
import { PageHeader } from "../components/common/PageHeader";
import { learningService } from "../services/learningService";

export function JLPTLevelsPage() {
  const levels = learningService.getLevels();

  return (
    <div className="page-stack">
      <PageHeader
        eyebrow="Lộ trình"
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
