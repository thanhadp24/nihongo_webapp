import { BookOpen, Dumbbell, LibraryBig } from "lucide-react";
import { Link, Navigate, useParams } from "react-router";
import { Breadcrumb } from "../components/common/Breadcrumb";
import { PageHeader } from "../components/common/PageHeader";
import { ProgressBar } from "../components/common/ProgressBar";
import { learningService } from "../services/learningService";

export function TopicDetailPage() {
  const { chapterId = "", levelId = "", topicId = "" } = useParams();
  const level = learningService.getLevel(levelId);
  const chapter = learningService.getChapter(chapterId);
  const topic = learningService.getTopic(topicId);
  const topicVocabulary = learningService.getTopicVocabulary(topicId);
  const topicLessons = learningService.getTopicLessons(topicId);

  if (!level || !chapter || !topic) return <Navigate to="/jlpt" replace />;

  return (
    <div className="page-stack">
      <Breadcrumb
        items={[
          { label: "Trang chủ", to: "/" },
          { label: level.name, to: `/jlpt/${level.id}` },
          { label: `Chapter ${chapter.chapterNumber}`, to: `/jlpt/${level.id}/chapters/${chapter.id}` },
          { label: topic.title }
        ]}
      />
      <PageHeader
        actions={
          <Link className="primary-button" to={`/jlpt/${level.id}/chapters/${chapter.id}/topics/${topic.id}/vocabulary`}>
            Bắt đầu học
          </Link>
        }
        eyebrow={`${level.name} • Chapter ${chapter.chapterNumber}`}
        subtitle={topic.description}
        title={topic.title}
      />
      <section className="topic-overview">
        <div className="overview-main">
          <p className="japanese-title-small">{topic.japaneseTitle}</p>
          <div className="stat-row roomy">
            <span><LibraryBig aria-hidden="true" /> {topicVocabulary.length} từ vựng</span>
            <span><BookOpen aria-hidden="true" /> {topicLessons.length} bài học</span>
            <span><Dumbbell aria-hidden="true" /> {topic.exerciseCount} luyện tập</span>
          </div>
          <ProgressBar label="Tiến độ chủ đề" value={topic.progress} />
        </div>
        <div className="content-tabs">
          <Link to={`/jlpt/${level.id}/chapters/${chapter.id}/topics/${topic.id}`}>Tổng quan</Link>
          <Link to={`/jlpt/${level.id}/chapters/${chapter.id}/topics/${topic.id}/vocabulary`}>Từ vựng</Link>
          <Link to={`/jlpt/${level.id}/chapters/${chapter.id}/topics/${topic.id}/lessons`}>Bài học</Link>
          <Link to={`/jlpt/${level.id}/chapters/${chapter.id}/topics/${topic.id}/lessons`}>Ngữ pháp</Link>
          <Link to="/review">Luyện tập</Link>
        </div>
      </section>
    </div>
  );
}
