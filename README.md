# 備品管理・貸出管理アプリ
- FastAPI + PostgreSQL + nginx をバックエンドに、Vue3/Vuetify を nginx でホストするシングルページアプリ構成
- MVP の設計に基づき、総務による備品登録・貸出・返却、社員一覧閲覧、ユーザー管理を備えた構成
- Playwright を使った E2E テストを `test_playwright` プロファイルで docker compose から実行可能

## 起動
すべてのコンポーネントは docker compose で起動します。

```
docker compose up --build
```

`frontend` サービス: `http://localhost:4173`（nginxが Vue アプリをサーブ）

`backend` サービス: `http://localhost:8000/api`（nginx経由で FastAPI を公開）

`db` サービス: PostgreSQL（認証:postgres/postgres, データベース: asset_db）

## 環境変数
- `SECRET_KEY`, `DATABASE_URL`, `ADMIN_EMAIL`, `ADMIN_PASSWORD` は `backend` サービスで利用され、`.env` や compose 上書きで変更可能
- `VITE_API_BASE` は `frontend` サービスで `/api` を指すよう設定

## テスト
### 単体/統合
- FastAPI および Vue の単体テストは未実装（MVP の振る舞いを E2E で確認）

### E2E テスト (Playwright)
E2E テストは Playwright を使い `frontend` の UI を通じてアプリを検証します。docker compose の `test_playwright` プロファイルを使って以下のように実行します。

```
docker compose --profile test run --rm test_playwright
```

このコマンドは `test_playwright` サービスを起動し、`npm install` → `npx playwright install chromium` → `npm run test` を実行します。

## コード構成
- `backend/`: FastAPI + SQLAlchemy + JWT + nginx reverse proxy
- `frontend/`: Vite/Vue3/Vuetify アプリを nginx で提供
- `e2e/`: Playwright のテストコードおよび設定
- `docker-compose.yml`: `backend`, `frontend`, `db`, `test_playwright` を定義
- `docs/detail_design.md`: 詳細設計書

## 開発サイクル
1. `docker compose up --build` で環境を起動
2. `frontend` にログイン: `admin@example.com` / `adminpassword`
3. 利用シナリオに基づき備品登録・貸出・返却・ユーザー管理を操作
4. E2E テストは `docker compose --profile test run --rm test_playwright` で常にパスするように保守
