# 備品管理・貸出予約アプリ

## 起動手順（docker-compose）

```bash
docker compose up --build
```

- バックエンド: http://localhost:8000
- フロントエンド: http://localhost:5173
- 初期管理者: admin@example.com / AdminPass123

## バックエンド手動起動（ローカル）

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL=postgresql+asyncpg://app:app@localhost:5432/app
export ADMIN_EMAIL=admin@example.com
export ADMIN_PASSWORD=AdminPass123
uvicorn backend.app.main:app --reload
```

## フロントエンド起動（ローカル）

```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0 --port 5173
```

## 主なエンドポイント
- POST /auth/login
- POST /auth/users (admin)
- GET /items, POST /items, PUT /items/{id} (adminで作成/更新)
- GET /reservations, POST /reservations, POST /reservations/{id}/cancel
- POST /loans, POST /loans/{id}/return, GET /loans/overdue (admin)
- GET /users (admin)

## テスト

```bash
cd backend
pytest
```

## 注意
- 本番運用時は SECRET_KEY, ADMIN_PASSWORD を環境変数で必ず上書きしてください。
