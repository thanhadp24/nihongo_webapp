# PWA Offline Design

Offline data is split by storage type:

- Cache Storage: HTML, CSS, JavaScript, icons, images, audio, and static assets.
- IndexedDB: downloaded lesson JSON, user progress, metadata, and sync queue.

The server remains the source of truth. IndexedDB stores local copies and pending user changes.

