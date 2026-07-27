import type { LearningStatus } from "../types/learning";

export const statusLabels: Record<LearningStatus, string> = {
  NOT_STARTED: "Chưa học",
  IN_PROGRESS: "Đang học",
  COMPLETED: "Đã hoàn thành",
  REVIEW_REQUIRED: "Cần ôn tập",
  LOCKED: "Đang khóa"
};

export function clampProgress(value: number) {
  return Math.min(100, Math.max(0, value));
}

export function actionLabel(status: LearningStatus) {
  if (status === "COMPLETED") return "Ôn tập lại";
  if (status === "REVIEW_REQUIRED") return "Ôn tập";
  if (status === "IN_PROGRESS") return "Tiếp tục";
  if (status === "LOCKED") return "Đang khóa";
  return "Bắt đầu học";
}
