# 備品管理・貸出予約アプリ

## 概要
FastAPI + PostgreSQL + Vue3(Vuetify)による備品管理・貸出予約システムです。要件/詳細設計は `doc/requirements.md` / `doc/detailed_design.md` を参照。

## 構成
- backend: FastAPI (uvicorn), SQLAlchemy, PostgreSQL
- frontend: Vue3 + Vite + Vuetify + Pinia
- docker-compose: api/db/frontend を起動

## 起動手順
```bash
docker-compose up --build
```
起動後:
- API: http://localhost:8000
- Frontend: http://localhost:5173

初期管理者は環境変数で指定（docker-composeにデフォルト定義あり）:
- ADMIN_EMAIL=admin@example.com
- ADMIN_PASSWORD=adminpass123

## API概要
- 認証: POST /auth/login (JWT発行)
- ユーザー: /users (admin専用)
- 備品: /equipments
- 予約: /reservations
- 貸出: /lendings (admin)
- 返却: /returns (admin)
- 遅延一覧: /overdues (admin)
- バッチ: POST /jobs/mark-overdue (admin)

## テスト
```bash
cd backend
pytest
```

## 環境変数（主要）
- DATABASE_URL (例: postgresql+psycopg2://appuser:apppass@db:5432/appdb)
- JWT_SECRET
- ADMIN_EMAIL / ADMIN_PASSWORD

## ディレクトリ
- backend/app: API, services, repositories, models, schemas
- frontend/src: Vueコンポーネント、router
- doc: 要件・詳細設計
