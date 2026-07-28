import type { LearningStatus } from "../types/learning";

export function actionLabel(status: LearningStatus) {
  if (status === "COMPLETED") return "Ôn tập lại";
  if (status === "REVIEW_REQUIRED") return "Ôn tập";
  if (status === "IN_PROGRESS") return "Tiếp tục";
  if (status === "LOCKED") return "Đang khóa";
  return "Bắt đầu học";
}
