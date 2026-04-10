# 備品管理・貸出管理アプリ（MVP）

`docs/detail_design.md` と `tasks.md` に基づき、FastAPI + Vue 3 + Vuetify + PostgreSQL + Docker Compose で実装したサンプルです。

## 構成

```text
.
├── docker-compose.yml
├── src/
│   ├── backend/
│   │   ├── app/
│   │   └── tests/
│   └── frontend/
└── e2e/
```

## 起動

```bash
docker compose up --build
```

- フロントエンド: `http://localhost:4173`
- バックエンドヘルスチェック: `http://localhost:4173/api/health`

## 初期アカウント

- 総務: `admin@example.com` / `admin1234`
- 社員: `employee@example.com` / `employee1234`

## バックエンドテスト

```bash
cd src/backend
python -m pytest
```

## E2E テスト（Playwright）

```bash
docker compose --profile test run --rm test_playwright
```

## API 一覧

- `POST /api/auth/login`
- `GET /api/items`
- `POST /api/items`
- `PUT /api/items/{id}`
- `POST /api/items/{id}/loan`
- `POST /api/items/{id}/return`
- `GET /api/users`
- `GET /api/users/{id}`
- `POST /api/users`
- `PUT /api/users/{id}`
- `DELETE /api/users/{id}`

## E2E シナリオ表

| シナリオ | 目的 | 前提 | 手順 | 期待結果 |
|---|---|---|---|---|
| ログイン | 認証確認 | 初期総務ユーザーが存在 | ログインフォーム入力して送信 | 備品一覧へ遷移 |
| 備品一覧 | 状態可視化 | 初期データあり | 備品一覧表示 | 資産番号・名称・状態・貸出先が表示 |
| 備品登録 | 新規追加 | 総務ログイン | 備品登録ダイアログで保存 | 一覧に新規備品が表示 |
| 備品編集 | 情報更新 | 登録済み備品あり | 編集ダイアログで更新 | 一覧に更新値が反映 |
| 貸出処理 | 貸出開始 | 貸出可の備品あり | 貸出ダイアログで社員を選択 | 備品状態が貸出中 |
| 返却処理 | 返却完了 | 貸出中の備品あり | 返却ダイアログで確定 | 備品状態が貸出可 |
| ユーザー登録 | 追加作成 | 総務ログイン | ユーザー登録ダイアログで保存 | 一覧に新規ユーザー |
| ユーザー一覧 | 管理確認 | ユーザー複数件あり | 一覧表示 | 全ユーザーとステータス表示 |
| ユーザー詳細 | 情報確認 | 対象ユーザーあり | 詳細ボタン押下 | 詳細ダイアログ表示 |
| ユーザー編集 | 変更反映 | 対象ユーザーあり | 編集ダイアログで保存 | 一覧に更新値が反映 |
| ユーザー削除 | 論理削除 | 対象ユーザーあり | 削除ボタン押下 | ステータスが削除済 |
