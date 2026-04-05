# 備品管理・貸出管理アプリ 実装タスク一覧

## タスク一覧

### フェーズ1: プロジェクト基盤

| No | タスク | 完了条件 |
|----|--------|---------|
| 1-1 | docker-compose.yml 作成 | `docker compose build` がエラーなく完了すること |
| 1-2 | .env.example 作成 | ADMIN_LOGIN_ID / ADMIN_PASSWORD / JWT_SECRET_KEY / PLAYWRIGHT_PORT が定義されていること |
| 1-3 | backend/Dockerfile 作成 | `docker compose build backend` が成功すること |
| 1-4 | frontend/Dockerfile 作成（マルチステージ） | `docker compose build frontend` が成功すること |
| 1-5 | frontend/nginx.conf 作成（/api/ リバースプロキシ + SPAルーティング） | nginxが / と /api/ を正しくルーティングすること |

### フェーズ2: バックエンド実装

| No | タスク | 完了条件 |
|----|--------|---------|
| 2-1 | backend/common/errors.py 実装（共通例外クラス） | AppError / NotFoundError / ConflictError が定義されていること |
| 2-2 | backend/database.py 実装（DatabaseManager） | `init_db()` 実行でテーブル作成・初期管理者登録が完了すること |
| 2-3 | backend/models/ 実装（Pydantic スキーマ） | 全モデル（Equipment, LendingRecord, AdminUser）が定義されていること |
| 2-4 | backend/repositories/admin_user_repository.py 実装 | `find_by_login_id` が正しく動作すること |
| 2-5 | backend/repositories/equipment_repository.py 実装 | find_all / find_by_id / create / update / delete / update_status が正しく動作すること |
| 2-6 | backend/repositories/lending_repository.py 実装 | find_all / find_active_by_equipment_id / find_active_all / create / set_returned が正しく動作すること |
| 2-7 | backend/common/auth.py 実装（JWT生成・検証・Dependency） | 正常JWT検証・期限切れ拒否が動作すること |
| 2-8 | backend/services/auth_service.py 実装 | ログイン成功時JWT返却・失敗時例外が動作すること |
| 2-9 | backend/services/equipment_service.py 実装 | 全メソッド（get_all / create / update / delete）が業務ロジック通りに動作すること |
| 2-10 | backend/services/lending_service.py 実装 | lend / return_item がトランザクション込みで正しく動作すること |
| 2-11 | backend/routers/auth.py 実装 | POST /api/auth/login が正常/異常ともに正しいレスポンスを返すこと |
| 2-12 | backend/routers/equipment.py 実装 | 全エンドポイント（GET/POST/PUT/DELETE）が正しいレスポンスを返すこと |
| 2-13 | backend/routers/lending.py 実装 | 全エンドポイント（GET/POST/PUT）が正しいレスポンスを返すこと |
| 2-14 | backend/main.py 実装（FastAPI アプリ・CORS・ルーター登録・起動イベント） | `docker compose up backend` 起動後 `/api/equipment` にアクセスできること |

### フェーズ3: フロントエンド実装

| No | タスク | 完了条件 |
|----|--------|---------|
| 3-1 | package.json 作成（Vue3 / Vuetify3 / Pinia / vue-router / axios） | `npm install` が成功すること |
| 3-2 | frontend/src/api/client.js 実装（axios + 全API関数） | 全APIへのリクエスト関数が定義されていること。インターセプターでJWT付与・エラー処理が動作すること |
| 3-3 | frontend/src/stores/auth.js 実装（Pinia 認証ストア） | ログイン状態・トークン管理が動作すること |
| 3-4 | frontend/src/router/index.js 実装（ルーティング + ナビゲーションガード） | 未認証で S03〜S06 にアクセスするとS02にリダイレクトされること |
| 3-5 | frontend/src/pages/LoginPage.vue 実装（S02） | 正常ログインでS01に遷移し、エラー時にメッセージが表示されること |
| 3-6 | frontend/src/pages/EquipmentList.vue 実装（S01） | 未ログイン時はログインボタンのみ、ログイン時は全操作ボタンが表示されること |
| 3-7 | frontend/src/pages/EquipmentManagement.vue 実装（S03） | 備品の追加・編集・削除ダイアログが正しく動作すること。貸出中は削除ボタン非表示 |
| 3-8 | frontend/src/pages/LendingNew.vue 実装（S04） | 利用可能備品のみ選択可能。保存後S01に遷移すること |
| 3-9 | frontend/src/pages/LendingReturn.vue 実装（S05） | 貸出中記録のみ選択可能。保存後S01に遷移すること |
| 3-10 | frontend/src/pages/LendingHistory.vue 実装（S06） | 全履歴が一覧表示されること |
| 3-11 | frontend/src/main.js / App.vue 実装 | Vue アプリが正常に起動すること |

### フェーズ4: バリデーション（単体・結合テスト）

| No | タスク | 完了条件 |
|----|--------|---------|
| 4-1 | バックエンド単体テスト実装（pytest） | 設計書のテストケース一覧（正常・異常）が全て pass すること |
| 4-2 | バックエンド結合テスト実装（FastAPI TestClient） | 設計書のAPIテストケース一覧が全て pass すること |
| 4-3 | `docker compose up` での起動確認 | http://localhost にアクセスして備品一覧画面が表示されること |
| 4-4 | 初期管理者ログイン確認 | .env の認証情報でログインできること |

### フェーズ5: E2Eテスト設計・実装

| No | タスク | 完了条件 |
|----|--------|---------|
| 5-1 | e2e/playwright.config.js 作成 | Playwright設定ファイルが作成されていること |
| 5-2 | e2e/tests/scenarios.spec.js 実装 | 設計書のE2Eシナリオ T01〜T10 が全て実装されていること |
| 5-3 | `docker compose --profile test up --build` での起動確認 | test_playwright コンテナが起動し http://localhost:9999/mcp にアクセスできること |

### フェーズ6: E2Eテスト実行・修正

| No | タスク | 完了条件 |
|----|--------|---------|
| 6-1 | Playwright MCP経由でE2Eテスト実行（T01〜T10） | 全シナリオが成功すること。失敗した場合は実装を修正して再実行する |
| 6-2 | E2Eテスト全成功の確認 | T01〜T10 全シナリオが success になること |

### フェーズ7: 最終確認

| No | タスク | 完了条件 |
|----|--------|---------|
| 7-1 | 全変更点の実装漏れチェック | 設計書の全機能（F01〜F06）・全画面（S01〜S06）・全API・全クラスが実装されていること |
| 7-2 | README.md 記述完了 | 起動手順・E2Eテスト実行手順・Playwright MCP接続手順が記述されていること |
| 7-3 | .env.example が揃っていること | 必要な環境変数が全て定義されていること |
