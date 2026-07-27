import type { SavedContentItem, SavedContentType } from "../types/learning";

const storageKey = "nihongo.savedContent";
const eventName = "nihongo:saved-content-change";
let cachedRaw = "";
let cachedItems: SavedContentItem[] = [];

function makeKey(type: SavedContentType, id: string) {
  return `${type}:${id}`;
}

function readItems(): SavedContentItem[] {
  if (typeof window === "undefined") return [];

  try {
    const raw = window.localStorage.getItem(storageKey);
    if (!raw) {
      cachedRaw = "";
      cachedItems = [];
      return cachedItems;
    }
    if (raw === cachedRaw) return cachedItems;

    const parsed = JSON.parse(raw) as SavedContentItem[];
    cachedRaw = raw;
    cachedItems = Array.isArray(parsed)
      ? parsed.sort((a, b) => b.savedAt.localeCompare(a.savedAt))
      : [];
    return cachedItems;
  } catch {
    return [];
  }
}

function writeItems(items: SavedContentItem[]) {
  cachedItems = items.sort((a, b) => b.savedAt.localeCompare(a.savedAt));
  cachedRaw = JSON.stringify(cachedItems);
  window.localStorage.setItem(storageKey, cachedRaw);
  window.dispatchEvent(new Event(eventName));
}

export const savedContentService = {
  eventName,
  makeKey,

  getItems() {
    return readItems();
  },

  isSaved(type: SavedContentType, id: string) {
    const key = makeKey(type, id);
    return readItems().some((item) => item.key === key);
  },

  toggle(item: Omit<SavedContentItem, "key" | "savedAt">) {
    const key = makeKey(item.type, item.id);
    const current = readItems();
    const exists = current.some((saved) => saved.key === key);

    if (exists) {
      writeItems(current.filter((saved) => saved.key !== key));
      return false;
    }

    writeItems([
      {
        ...item,
        key,
        savedAt: new Date().toISOString()
      },
      ...current
    ]);
    return true;
  },

  remove(key: string) {
    writeItems(readItems().filter((item) => item.key !== key));
  },

  subscribe(callback: () => void) {
    window.addEventListener(eventName, callback);
    window.addEventListener("storage", callback);

    return () => {
      window.removeEventListener(eventName, callback);
      window.removeEventListener("storage", callback);
    };
  }
};
