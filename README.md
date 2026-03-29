# 備品管理システム

50人規模の会社向け備品貸出管理Webアプリです。

## 技術スタック

| レイヤー | 技術 |
|---|---|
| フロントエンド | Vue 3 + Vuetify 3 + Pinia + Vue Router 4 |
| バックエンド | FastAPI + SQLAlchemy 2 + Python 3.12 |
| データベース | PostgreSQL 16 |
| インフラ | Docker Compose + nginx |

## 起動方法

### 前提条件
- Docker および Docker Compose がインストールされていること

### 起動手順

```bash
# リポジトリのルートで実行
docker compose up --build
```

ブラウザで http://localhost にアクセスしてください。

### 初期ログイン情報

| 項目 | 値 |
|---|---|
| ログインID | `admin` |
| パスワード | `admin1234` |

> **注意**: 本番環境では必ずパスワードと `.env` の `SECRET_KEY` を変更してください。

## 画面一覧

| 画面 | URL | アクセス権限 |
|---|---|---|
| ログイン | `/login` | 全員 |
| ダッシュボード | `/` | 全員 |
| 備品一覧 | `/equipment` | 全員 |
| 備品登録 | `/equipment/create` | 管理者 |
| 備品編集 | `/equipment/:id/edit` | 管理者 |
| 貸出登録 | `/loans/create` | 管理者 |
| 返却登録 | `/loans/return` | 管理者 |
| ユーザー管理 | `/users` | 管理者 |
| ユーザー登録 | `/users/create` | 管理者 |

## API エンドポイント

```
POST   /api/auth/login
GET    /api/equipment/
POST   /api/equipment/
PUT    /api/equipment/{id}
DELETE /api/equipment/{id}
GET    /api/loans/
GET    /api/loans/active
POST   /api/loans/
PUT    /api/loans/{id}/return
GET    /api/users/
POST   /api/users/
PUT    /api/users/{id}
DELETE /api/users/{id}
```

## テスト実行

```bash
# バックエンドの依存をインストール
pip install -r backend/requirements.txt -r backend/requirements-dev.txt

# テスト実行
pytest
```

## 環境変数

`.env` ファイルで以下の変数を設定します：

| 変数名 | 説明 | デフォルト値 |
|---|---|---|
| `SECRET_KEY` | JWT署名秘密鍵 | `changeme-secret-key-please-change-in-production` |
| `DATABASE_URL` | PostgreSQL接続URL | `postgresql://appuser:apppassword@db:5432/equipment_db` |
| `POSTGRES_DB` | DBスキーマ名 | `equipment_db` |
| `POSTGRES_USER` | DBユーザー名 | `appuser` |
| `POSTGRES_PASSWORD` | DBパスワード | `apppassword` |

## ディレクトリ構成

```
.
├── docker-compose.yml
├── .env
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── main.py
│       ├── database.py
│       ├── dependencies.py
│       ├── init_db.py
│       ├── models/
│       ├── schemas/
│       ├── repositories/
│       ├── services/
│       └── routers/
├── frontend/
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── package.json
│   └── src/
│       ├── main.js
│       ├── App.vue
│       ├── api/
│       ├── router/
│       ├── stores/
│       └── views/
└── tests/
    ├── unit/backend/
    └── integration/backend/
```
