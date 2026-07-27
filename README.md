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

## Cách Chạy Hệ Thống

### Yêu Cầu

- Docker Desktop và Docker Compose
- Node.js 22+ nếu chạy frontend trực tiếp trên máy
- Python 3.12+ nếu chạy backend trực tiếp trên máy

### Chạy Nhanh Bằng Docker Compose

1. Tạo file môi trường từ file mẫu:

```powershell
Copy-Item .env.example .env
```

Nếu dùng Git Bash, macOS hoặc Linux:

```bash
cp .env.example .env
```

2. Khởi động toàn bộ hệ thống:

```bash
docker compose up --build
```

Hoặc dùng script có sẵn:

```powershell
scripts\start-dev.bat
```

Nếu dùng Git Bash, macOS hoặc Linux:

```bash
./scripts/start-dev.sh
```

3. Mở ứng dụng:

- Frontend: `http://localhost:5173`
- Backend health check: `http://localhost:8000/health`
- Backend API docs: `http://localhost:8000/docs`
- MySQL local port: `13306`

Lần đầu khởi động, MySQL sẽ tự nạp schema và seed data trong `database/schema` và `database/seed`.
Nếu backend báo database chưa sẵn sàng, đợi MySQL khởi động xong rồi refresh lại frontend hoặc gọi lại API.

### Dừng Hệ Thống

```bash
docker compose down
```

Nếu muốn xóa sạch database volume và nạp lại seed từ đầu:

```bash
docker compose down -v
docker compose up --build
```

### Xem Log

```bash
docker compose logs -f
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f mysql
```

### Chạy Từng Phần Để Dev

Chạy MySQL bằng Docker:

```bash
docker compose up -d mysql
```

Chạy backend trên máy:

```powershell
cd backend
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:DATABASE_URL="mysql+pymysql://nihongo:1234@127.0.0.1:13306/nihongo_webapp"
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Chạy frontend trên máy, trong terminal khác:

```powershell
cd frontend
npm install
npm run dev -- --host 0.0.0.0
```

Frontend đọc API từ biến `VITE_API_BASE_URL`. Mặc định dự án đang dùng:

```text
VITE_API_BASE_URL=http://localhost:8000/api
```

### Build Và Test

Frontend:

```bash
cd frontend
npm run build
npm run test
```

Backend hiện chưa có test runner riêng trong `requirements.txt`. Có thể kiểm tra nhanh API sau khi chạy backend:

```bash
curl http://localhost:8000/health
curl http://localhost:8000/api/jlpt-levels
```

## Documentation

- `docs/database-design.md`
- `docs/api-design.md`
- `docs/pwa-offline-design.md`
- `docs/project-structure.md`
- `plan/thiet-ke-du-lieu-pwa-hoc-tieng-nhat.md`

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
docker compose up -d mysql