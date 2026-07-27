import { BookOpen, Clock, Headphones, MessageCircle, PenTool, TestTube2 } from "lucide-react";
import { Link } from "react-router";
import type { Lesson } from "../../types/learning";
import { actionLabel } from "../../utils/learning";
import { ProgressBar } from "../common/ProgressBar";
import { StatusBadge } from "../common/StatusBadge";

const lessonIcons = {
  VOCABULARY: BookOpen,
  GRAMMAR: PenTool,
  KANJI: BookOpen,
  DIALOGUE: MessageCircle,
  LISTENING: Headphones,
  READING: BookOpen,
  TEST: TestTube2
};

export function LessonCard({ lesson }: { lesson: Lesson }) {
  const Icon = lessonIcons[lesson.type];

  return (
    <Link className="lesson-card" to={`/lessons/${lesson.id}`}>
      <div className="lesson-icon">
        <Icon aria-hidden="true" />
      </div>
      <div>
        <p className="eyebrow">Bài {String(lesson.lessonNumber).padStart(2, "0")}</p>
        <h2>{lesson.title}</h2>
        <p className="japanese-caption">{lesson.japaneseTitle}</p>
        <div className="stat-row">
          <span><Clock aria-hidden="true" /> {lesson.durationMinutes} phút</span>
          <span>{lesson.vocabularyCount} từ vựng</span>
          <span>{lesson.patternCount} mẫu câu</span>
        </div>
      </div>
      <div className="lesson-side">
        <StatusBadge status={lesson.status} />
        <ProgressBar label="Tiến độ" value={lesson.progress} />
        <span className="primary-button">{actionLabel(lesson.status)}</span>
      </div>
    </Link>
  );
}
