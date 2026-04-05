# 備品管理・貸出管理アプリ

Vue 3 + FastAPI + SQLite による備品管理・貸出記録アプリです。

---

## 技術スタック

| 区分 | 技術 |
|------|------|
| フロントエンド | Vue 3 + Vuetify 3 + Pinia + vue-router + axios |
| バックエンド | Python 3.12 + FastAPI + SQLite |
| 認証 | JWT (HS256, 8時間有効) + bcrypt |
| インフラ | Docker Compose + nginx (リバースプロキシ) |
| テスト | pytest (単体・結合), Playwright MCP (E2E) |

---

## 起動方法

### 1. 環境変数の設定

```bash
cp .env.example .env
# 必要に応じて .env を編集する
```

`.env.example` の内容:

| 変数名 | 説明 | デフォルト例 |
|--------|------|------------|
| `ADMIN_LOGIN_ID` | 初期管理者ログインID | `admin` |
| `ADMIN_PASSWORD` | 初期管理者パスワード | `AdminPass123` |
| `JWT_SECRET_KEY` | JWT署名キー（本番環境では必ず変更） | `change-me-in-production` |
| `PLAYWRIGHT_PORT` | Playwright MCPサーバーポート | `9999` |

### 2. 起動

```bash
docker compose up --build
```

### 3. アクセス

- アプリ: http://localhost
- 初期管理者ログイン: `.env` の `ADMIN_LOGIN_ID` / `ADMIN_PASSWORD` を参照

---

## バックエンドテスト（pytest）

```bash
docker compose run --rm --no-deps backend python -m pytest tests/ -v
```

---

## E2Eテスト（Playwright MCP）

### 1. testプロファイルで全サービス起動

```bash
docker compose --profile test up --build
```

### 2. MCP接続エンドポイント

```
http://localhost:9999/mcp
```

### 3. AIエージェントへのMCP設定

**GitHub Copilot (VS Code)** — `.vscode/mcp.json` に追加:

```json
{
  "servers": {
    "test_playwright": {
      "type": "http",
      "url": "http://localhost:9999/mcp"
    }
  }
}
```

**Claude Code**:

```bash
claude mcp add --transport http test_playwright http://localhost:9999/mcp
```

### 4. E2Eシナリオ一覧 (T01〜T10)

| No | シナリオ |
|----|---------|
| T01 | 一般ユーザーが備品一覧を閲覧する |
| T02 | 総務担当者がログインする |
| T03 | 総務担当者が備品を登録する |
| T04 | 総務担当者が備品を編集する |
| T05 | 総務担当者が備品を削除する |
| T06 | 貸出記録を登録する |
| T07 | 返却記録を登録する |
| T08 | 貸出履歴を確認する |
| T09 | 未ログイン時に操作ボタンが非表示 |
| T10 | ログアウトする |

---

## ドキュメント

- [要件定義書](doc/requirements.md)
- [詳細設計書](doc/detail_design.md)
- [実装タスク](.history/20260406-備品管理アプリ実装/tasks.md)

