# Nihongo Webapp

PWA for learning Japanese with a Python backend, MySQL database, and React/Vite frontend.

## Project Layout

```text
backend/      Python REST API, migrations, media, and backend tests
frontend/     React + Vite PWA source, public assets, and frontend tests
database/     SQL schema, seed data, and import files
docs/         Database, API, offline/PWA, and project structure notes
scripts/      Local development and maintenance scripts
plan/         Planning and design drafts
```

## Stack

- Backend: Python, FastAPI, SQLAlchemy, Alembic, MySQL
- Frontend: React, Vite, TypeScript, React Router, TanStack Query, Dexie.js, Workbox
- Database: MySQL

## Getting Started

1. Copy `.env.example` into backend/frontend environment files as needed.
2. Start the local stack with Docker Compose:

```bash
docker compose up --build
```

3. Backend will be prepared for `http://localhost:8000`.
4. Frontend will be prepared for `http://localhost:5173`.

## Documentation

- `docs/database-design.md`
- `docs/api-design.md`
- `docs/pwa-offline-design.md`
- `docs/project-structure.md`
- `plan/thiet-ke-du-lieu-pwa-hoc-tieng-nhat.md`

