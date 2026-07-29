import { Navigate, Route, Routes } from "react-router";
import { MainLayout } from "./layouts/MainLayout";
import { ChaptersPage } from "./pages/ChaptersPage";
import { FavoritesPage } from "./pages/FavoritesPage";
import { GrammarFlashcardsPage } from "./pages/GrammarFlashcardsPage";
import { GrammarPage } from "./pages/GrammarPage";
import { HomePage } from "./pages/HomePage";
import { JLPTLevelsPage } from "./pages/JLPTLevelsPage";
import { KanjiDetailPage } from "./pages/KanjiDetailPage";
import { KanjiFlashcardsPage } from "./pages/KanjiFlashcardsPage";
import { KanjiImageViewerPage } from "./pages/KanjiImageViewerPage";
import { KanjiPage } from "./pages/KanjiPage";
import { LevelVocabularyPage } from "./pages/LevelVocabularyPage";
import { LessonDetailPage } from "./pages/LessonDetailPage";
import { LessonsPage } from "./pages/LessonsPage";
import { PlaceholderPage } from "./pages/PlaceholderPage";
import { TopicDetailPage } from "./pages/TopicDetailPage";
import { TopicsPage } from "./pages/TopicsPage";
import { VocabularyFlashcardsPage } from "./pages/VocabularyFlashcardsPage";
import { VocabularyPage } from "./pages/VocabularyPage";

function App() {
  return (
    <Routes>
      <Route element={<MainLayout />}>
        <Route element={<HomePage />} path="/" />
        <Route element={<JLPTLevelsPage />} path="/jlpt" />
        <Route element={<ChaptersPage />} path="/jlpt/:levelId" />
        <Route element={<LevelVocabularyPage />} path="/jlpt/:levelId/vocabulary" />
        <Route element={<VocabularyFlashcardsPage />} path="/jlpt/:levelId/vocabulary/flashcards" />
        <Route element={<GrammarPage />} path="/jlpt/:levelId/grammar" />
        <Route element={<GrammarFlashcardsPage />} path="/jlpt/:levelId/grammar/flashcards" />
        <Route element={<KanjiPage />} path="/jlpt/:levelId/kanji" />
        <Route element={<KanjiImageViewerPage />} path="/jlpt/:levelId/kanji/images" />
        <Route element={<KanjiFlashcardsPage />} path="/jlpt/:levelId/kanji/flashcards" />
        <Route element={<KanjiDetailPage />} path="/kanji/:kanjiId" />
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
          element={<VocabularyFlashcardsPage />}
          path="/jlpt/:levelId/chapters/:chapterId/topics/:topicId/vocabulary/flashcards"
        />
        <Route
          element={<LessonsPage />}
          path="/jlpt/:levelId/chapters/:chapterId/topics/:topicId/lessons"
        />
        <Route element={<LessonDetailPage />} path="/lessons/:lessonId" />
        <Route element={<PlaceholderPage title="Luyện đọc" />} path="/reading" />
        <Route element={<PlaceholderPage title="Luyện nghe" />} path="/listening" />
        <Route element={<PlaceholderPage title="Ôn tập" />} path="/review" />
        <Route element={<FavoritesPage />} path="/favorites" />
        <Route element={<PlaceholderPage title="Tài khoản" />} path="/profile" />
        <Route element={<Navigate to="/" replace />} path="*" />
      </Route>
    </Routes>
  );
}

export default App;
