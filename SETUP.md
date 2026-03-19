# 起動手順 (ローカル開発)

## 前提
- Node.js (推奨: v18+)
- PostgreSQL がローカルで利用可能であること

## 1. リポジトリ直下の準備
```bash
# 依存は backend と frontend それぞれでインストールする
cd backend && npm install
cd ../frontend && npm install
```

## 2. 環境変数の設定 (backend)
`backend/.env.sample` をコピーして `.env` を作成し、必須値を設定します。

例:
```env
DATABASE_URL=postgres://user:password@localhost:5432/asset_booking
JWT_SECRET=change_me_secret
PORT=3000
PASSWORD_EXPIRE_DAYS=90
PASSWORD_MIN_LENGTH=8
```

## 3. データベース初期化
PostgreSQL でスキーマを流し込みます。

```bash
cd backend
psql "$DATABASE_URL" -f db/schema.sql
```

## 4. バックエンド起動
```bash
cd backend
npm run dev
```
サーバーが `PORT` (デフォルト 3000) で起動します。

## 5. フロントエンド起動
別ターミナルで:
```bash
cd frontend
npm run dev
```
Vite 開発サーバーが `http://localhost:5173` で起動します。
API は `/api` へのリクエストをバックエンドへプロキシする想定です。必要に応じて `vite.config.ts` の proxy 設定を有効化してください。

## 6. 動作確認
- ブラウザで `http://localhost:5173` にアクセス
- ログイン後、備品一覧や予約作成を試行

## トラブルシュート
- `DATABASE_URL が未設定` エラー: backend/.env を作成し DATABASE_URL を設定してください。
- DB 接続エラー: 接続先ホスト/ユーザー/パスワード/DB名を見直してください。
- `ECONNREFUSED 127.0.0.1:5432`（Docker起動時）: ルート `.env` の DATABASE_URL が `localhost` になっているとコンテナ内から接続できません。`postgres://app:app@db:5432/asset_booking` に修正し、`docker compose up --build` で再起動してください。
- `ECONNREFUSED ::1:5432`（ローカル）: PostgreSQL サーバが起動しているか確認し、`pg_isready` または `psql "$DATABASE_URL" -c 'select 1'` で疎通を確認してください。IPv6 ::1 に接続できない場合は DATABASE_URL を `postgres://user:pass@127.0.0.1:5432/dbname` のように明示します。
