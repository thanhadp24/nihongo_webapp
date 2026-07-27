import { Navigate, Route, Routes } from "react-router";
import { MainLayout } from "./layouts/MainLayout";
import { ChaptersPage } from "./pages/ChaptersPage";
import { HomePage } from "./pages/HomePage";
import { JLPTLevelsPage } from "./pages/JLPTLevelsPage";
import { LessonDetailPage } from "./pages/LessonDetailPage";
import { LessonsPage } from "./pages/LessonsPage";
import { PlaceholderPage } from "./pages/PlaceholderPage";
import { TopicDetailPage } from "./pages/TopicDetailPage";
import { TopicsPage } from "./pages/TopicsPage";
import { VocabularyPage } from "./pages/VocabularyPage";

function App() {
  return (
    <Routes>
      <Route element={<MainLayout />}>
        <Route element={<HomePage />} path="/" />
        <Route element={<JLPTLevelsPage />} path="/jlpt" />
        <Route element={<ChaptersPage />} path="/jlpt/:levelId" />
        <Route element={<TopicsPage />} path="/jlpt/:levelId/chapters/:chapterId" />
        <Route
          element={<TopicDetailPage />}
          path="/jlpt/:levelId/chapters/:chapterId/topics/:topicId"
        />
        <Route
          element={<VocabularyPage />}
          path="/jlpt/:levelId/chapters/:chapterId/topics/:topicId/vocabulary"
        />
        <Route
          element={<LessonsPage />}
          path="/jlpt/:levelId/chapters/:chapterId/topics/:topicId/lessons"
        />
        <Route element={<LessonDetailPage />} path="/lessons/:lessonId" />
        <Route element={<PlaceholderPage title="Ôn tập" />} path="/review" />
        <Route element={<PlaceholderPage title="Nội dung đã lưu" />} path="/favorites" />
        <Route element={<PlaceholderPage title="Tiến độ học tập" />} path="/progress" />
        <Route element={<PlaceholderPage title="Tài khoản" />} path="/profile" />
        <Route element={<Navigate to="/" replace />} path="*" />
      </Route>
    </Routes>
  );
}

export default App;
