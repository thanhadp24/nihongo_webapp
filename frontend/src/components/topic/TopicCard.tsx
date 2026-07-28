import { BookOpen, CalendarDays, Globe2, Home, IdCard, MessagesSquare } from "lucide-react";
import { Link } from "react-router";
import type { Topic } from "../../types/learning";
import { actionLabel } from "../../utils/learning";

const topicIcons = {
  greetings: MessagesSquare,
  profile: IdCard,
  world: Globe2,
  home: Home,
  calendar: CalendarDays
};

export function TopicCard({ topic }: { topic: Topic }) {
  const Icon = topicIcons[topic.illustration as keyof typeof topicIcons] ?? BookOpen;

  return (
    <Link
      className="topic-card"
      to={`/jlpt/${topic.levelId}/chapters/${topic.chapterId}/topics/${topic.id}`}
    >
      <div className="topic-art">
        <Icon aria-hidden="true" />
      </div>
      <div className="card-title-row">
        <div>
          <p className="eyebrow">Chủ đề {String(topic.topicNumber).padStart(2, "0")}</p>
          <h2>{topic.title}</h2>
          <p className="japanese-caption">{topic.japaneseTitle}</p>
        </div>
      </div>
      <p>{topic.description}</p>
      <div className="stat-row">
        <span>{topic.vocabularyCount} từ vựng</span>
        <span>{topic.lessonCount} bài học</span>
        <span>{topic.exerciseCount} luyện tập</span>
      </div>
      <span className="primary-button">{actionLabel(topic.status)}</span>
    </Link>
  );
}
