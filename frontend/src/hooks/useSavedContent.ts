import { useSyncExternalStore } from "react";
import { savedContentService } from "../services/savedContentService";
import type { SavedContentItem } from "../types/learning";

const emptyItems: SavedContentItem[] = [];

function emptySubscribe() {
  return () => undefined;
}

export function useSavedContent() {
  const items = useSyncExternalStore(
    typeof window === "undefined" ? emptySubscribe : savedContentService.subscribe,
    savedContentService.getItems,
    () => emptyItems
  );

  return items;
}

export function useSavedState(type: "vocabulary" | "kanji", id: string) {
  return useSyncExternalStore(
    typeof window === "undefined" ? emptySubscribe : savedContentService.subscribe,
    () => savedContentService.isSaved(type, id),
    () => false
  );
}
