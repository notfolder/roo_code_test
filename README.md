# 備品・貸出管理システム

社内の備品貸出状況をリアルタイムで管理するWebアプリケーションです。

---

## システム概要

- 備品の登録・編集・削除
- 貸出・返却記録の管理
- 備品一覧・貸出履歴の閲覧
- ユーザーアカウント管理（管理者／一般ユーザー）

## 前提条件

- Docker
- docker compose

## セットアップ手順

1. `.env` ファイルを作成します:

```bash
cp .env.example .env
```

2. 必要に応じて `.env` を編集してください（本番環境では `SECRET_KEY` を変更すること）。

## 起動方法

```bash
docker compose up -d
```

ブラウザで http://localhost にアクセスしてください。

初回起動時に `.env` の `INITIAL_ADMIN_LOGIN_ID` / `INITIAL_ADMIN_PASSWORD` で指定した管理者アカウントが自動生成されます。

## E2Eテスト実行方法

```bash
docker compose --profile test up -d
docker compose run --rm -e BASE_URL=http://frontend test_playwright sh -c "npm install && npx playwright test"
```

## 環境変数一覧

| 変数名 | 説明 | 例 |
|--------|------|----|
| `SECRET_KEY` | JWT署名用シークレットキー（64文字以上推奨） | ランダム文字列 |
| `INITIAL_ADMIN_LOGIN_ID` | 初期管理者ログインID | admin |
| `INITIAL_ADMIN_PASSWORD` | 初期管理者パスワード | password |

---

# roo_code_test
roo codeで仕様書から詳細設計、コードを生成するテスト
