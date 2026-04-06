# 備品・貸出管理システム 実装タスク一覧

---

## タスク一覧

### TASK-01: プロジェクト構成の作成
- **内容**: ディレクトリ構成・docker-compose.yml・.env.example の作成
- **完了条件**: `docker compose build` がエラーなく完了すること
- **バリデーション**: `docker compose config` でYAML構文エラーがないこと

### TASK-02: バックエンド - database.py
- **内容**: SQLAlchemy エンジン・セッション・Base定義。SQLite外部キー有効化（PRAGMA foreign_keys=ON）
- **完了条件**: `from app.database import engine, SessionLocal, Base` がエラーなくimportできること
- **バリデーション**: `python -c "from app.database import Base"` が成功すること

### TASK-03: バックエンド - models/
- **内容**: User・Item・LendingRecord の SQLAlchemy モデル定義
- **完了条件**: 全モデルがimportできること・テーブル定義が設計書と一致すること
- **バリデーション**: UT07（ItemService.get_items）がモデルを正しく参照できること

### TASK-04: バックエンド - schemas/
- **内容**: LoginRequest・TokenResponse・UserCreate・UserResponse・ItemCreate・ItemUpdate・ItemResponse・LendingRecordCreate・ReturnRequest・LendingRecordResponse の Pydantic スキーマ定義
- **完了条件**: 全スキーマがimportできること
- **バリデーション**: バリデーションエラー時に422が返ること（必須フィールドを省いたリクエストをPOST /api/itemsに送信して確認）

### TASK-05: バックエンド - services/auth_service.py
- **内容**: AuthService（authenticate_user・create_access_token・verify_token）実装
- **完了条件**: UT01〜UT06がすべてpass
- **バリデーション**: `pytest tests/test_auth_service.py` が全件pass

### TASK-06: バックエンド - services/item_service.py
- **内容**: ItemService（get_items・get_item・create_item・update_item・delete_item）実装
- **完了条件**: UT07〜UT12がすべてpass
- **バリデーション**: `pytest tests/test_item_service.py` が全件pass

### TASK-07: バックエンド - services/lending_service.py
- **内容**: LendingService（get_lending_records・create_lending_record・return_item）実装。貸出・返却の同一トランザクション処理を含む。get_lending_recordsはS05ではreturn_date IS NULLのレコードをフロントエンドでフィルタリングして使用する
- **完了条件**: UT13〜UT17がすべてpass
- **バリデーション**: `pytest tests/test_lending_service.py` が全件pass

### TASK-08: バックエンド - services/user_service.py
- **内容**: UserService（get_users・create_user・delete_user・get_user_by_login_id）実装
- **完了条件**: UT18〜UT22がすべてpass
- **バリデーション**: `pytest tests/test_user_service.py` が全件pass

### TASK-09: バックエンド - dependencies.py
- **内容**: get_db・get_current_user・require_admin の Dependency 実装
- **完了条件**: 未認証アクセスで401・一般ユーザーの管理者専用APIで403が返ること
- **バリデーション**: IT04・IT06の結合テストがpass

### TASK-10: バックエンド - routers/auth.py
- **内容**: POST /api/auth/login エンドポイント実装
- **完了条件**: IT01・IT02がpass
- **バリデーション**: `pytest tests/test_api_auth.py` が全件pass

### TASK-11: バックエンド - routers/items.py
- **内容**: GET/POST/PUT/DELETE /api/items エンドポイント実装
- **完了条件**: IT03〜IT10がすべてpass
- **バリデーション**: `pytest tests/test_api_items.py` が全件pass

### TASK-12: バックエンド - routers/lending_records.py
- **内容**: GET/POST /api/lending_records・PUT /api/lending_records/{id}/return エンドポイント実装
- **完了条件**: IT11〜IT16がpass
- **バリデーション**: `pytest tests/test_api_lending.py` が全件pass

### TASK-13: バックエンド - routers/users.py
- **内容**: GET/POST/DELETE /api/users エンドポイント実装
- **完了条件**: IT17〜IT23がpass
- **バリデーション**: `pytest tests/test_api_users.py` が全件pass

### TASK-14: バックエンド - main.py
- **内容**: FastAPIアプリ初期化・全ルーター登録・CORS設定・起動時初期管理者アカウント自動生成（環境変数から取得）
- **完了条件**: `docker compose up backend` でサービスが起動し、/api/docs にアクセスできること
- **バリデーション**: 初回起動で初期管理者アカウントが生成されること

### TASK-15: バックエンド - Dockerfile・requirements.txt
- **内容**: Python 3.11 ベースの Dockerfile・依存パッケージ一覧作成
- **完了条件**: `docker compose build backend` が成功すること
- **バリデーション**: ビルドエラーなし

### TASK-16: フロントエンド - package.json・vite.config.js
- **内容**: Vue3・Vuetify3・Pinia・axios・Vue Router の依存定義・Vite設定
- **完了条件**: `npm install` がエラーなく完了すること
- **バリデーション**: `npm run build` がエラーなく成功すること

### TASK-17: フロントエンド - src/api/client.js
- **内容**: axiosインスタンス作成（baseURL=/api/）・JWTヘッダー付与インターセプター・401時ログアウト処理
- **完了条件**: 全APIリクエストに Authorization ヘッダーが付与されること
- **バリデーション**: 401レスポンス時に/loginへリダイレクトされること（E2Eテスト）

### TASK-18: フロントエンド - stores/
- **内容**: useAuthStore・useItemStore・useLendingStore・useUserStore の実装
- **完了条件**: 各StoreがAPIを正しく呼び出しデータを保持すること
- **バリデーション**: E2EテストT02・T03でログイン後の状態が正しく管理されること

### TASK-19: フロントエンド - router/index.js
- **内容**: 全7ルート定義・ナビゲーションガード（未認証→/login、一般ユーザーの管理者専用ルート→/）実装
- **完了条件**: T01・T15のE2Eテストがpass
- **バリデーション**: `npx playwright test` でT01・T15がpass

### TASK-20: フロントエンド - components/AppBar.vue
- **内容**: ナビゲーションバー（管理者のみ管理ボタン表示・ログアウトボタン）実装
- **完了条件**: T02（管理者：全ボタン表示）・T03（一般：履歴・ログアウトのみ）がpass
- **バリデーション**: E2EテストT02・T03がpass

### TASK-21: フロントエンド - components/ConfirmDialog.vue
- **内容**: 汎用削除確認ダイアログ実装（props: title, message; emit: confirm, cancel）
- **完了条件**: S03・S07の削除ボタンクリック時にダイアログが表示されること
- **バリデーション**: E2EテストT06・T12でダイアログ操作が成功

### TASK-22: フロントエンド - components/ItemFormDialog.vue
- **内容**: 備品追加・編集ダイアログ実装（管理番号・備品名入力フォーム）
- **完了条件**: T04・T05のE2Eテストがpass
- **バリデーション**: E2EテストT04・T05がpass

### TASK-23: フロントエンド - components/UserFormDialog.vue
- **内容**: ユーザー追加ダイアログ実装（ログインID・パスワード・ロール選択フォーム）
- **完了条件**: T11のE2Eテストがpass
- **バリデーション**: E2EテストT11がpass

### TASK-24: フロントエンド - views/LoginView.vue
- **内容**: S02ログイン画面実装（ログインID・PW入力・ログインボタン・エラーメッセージ）
- **完了条件**: T02・T17のE2Eテストがpass
- **バリデーション**: E2EテストT02・T17がpass

### TASK-25: フロントエンド - views/ItemListView.vue
- **内容**: S01備品一覧画面実装（備品テーブル・管理者ボタン群・履歴・ログアウト）
- **完了条件**: T02・T03・T07・T08のE2Eテストがpass
- **バリデーション**: 備品の状態（利用可能/貸出中）と借用者名が正しく表示されること

### TASK-26: フロントエンド - views/ItemManageView.vue
- **内容**: S03備品管理画面実装（一覧・追加・編集・削除）
- **完了条件**: T04・T05・T06・T14のE2Eテストがpass
- **バリデーション**: E2EテストT04〜T06・T14がpass

### TASK-27: フロントエンド - views/LendView.vue
- **内容**: S04貸出登録画面実装（利用可能備品セレクト・登録ユーザーセレクト・貸出日・登録）
- **完了条件**: T07のE2Eテストがpass
- **バリデーション**: E2EテストT07がpass

### TASK-28: フロントエンド - views/ReturnView.vue
- **内容**: S05返却登録画面実装（貸出中記録セレクト・返却日・登録）
- **完了条件**: T08のE2Eテストがpass
- **バリデーション**: E2EテストT08がpass

### TASK-29: フロントエンド - views/HistoryView.vue
- **内容**: S06貸出履歴画面実装（全貸出記録テーブル・戻るボタン）
- **完了条件**: T09のE2Eテストがpass
- **バリデーション**: E2EテストT09がpass

### TASK-30: フロントエンド - views/UserManageView.vue
- **内容**: S07ユーザーアカウント管理画面実装（一覧・追加・削除）
- **完了条件**: T11・T12・T13・T16のE2Eテストがpass
- **バリデーション**: E2EテストT11〜T13・T16がpass

### TASK-31: フロントエンド - App.vue・main.js
- **内容**: ルートコンポーネント・Vue/Vuetify/Pinia/Router初期化・localStorageからのトークン復元
- **完了条件**: `npm run build` が成功しアプリが起動すること
- **バリデーション**: ビルドエラーなし・ページリロード後もログイン状態が維持されること

### TASK-32: フロントエンド - Dockerfile・nginx.conf
- **内容**: マルチステージビルド（node:20-alpine → nginx:alpine）・nginxの/api/リバースプロキシ設定（proxy_pass http://backend:8000 ※末尾スラッシュなし。スラッシュありだとnginxが/api/プレフィックスを除去し、FastAPIの/api/...ルートに到達できなくなるため）
- **完了条件**: `docker compose build frontend` が成功し、ブラウザからアクセスできること
- **バリデーション**: `curl http://localhost/api/items` がバックエンドに到達すること

### TASK-33: E2Eテスト - e2e/package.json
- **内容**: @playwright/test@1.59.0 の依存定義
- **完了条件**: `npm install` がエラーなく完了すること
- **バリデーション**: `npx playwright --version` が 1.59.0 を返すこと

### TASK-34: E2Eテスト - e2e/tests/scenarios.spec.js
- **内容**: T01〜T17の全シナリオをPlaywrightで実装。Vuetify data-testidの入力操作は `locator('[data-testid="xxx"] input').fill()` パターンを使用
- **完了条件**: T01〜T17全件のテストコードが実装されること
- **バリデーション**: `docker compose run --rm -e BASE_URL=http://frontend test_playwright sh -c "npm install && npx playwright test"` で全件pass

### TASK-35: README.md
- **内容**: システム概要・前提条件・セットアップ手順・起動方法・E2Eテスト実行方法・環境変数一覧の記述
- **完了条件**: README.mdが存在し、手順通りに操作してシステムが正常起動すること
- **バリデーション**: READMEの手順を最初から実行してE2Eテストが全件pass

### TASK-36: 全変更点の実装確認（最終）
- **内容**: 設計書の全セクションと実装の対応を確認する
- **完了条件**: 以下が全て満たされること
  - 機能F01〜F11が全て実装されていること
  - 画面S01〜S07が全て実装されていること
  - APIエンドポイント11本が全て実装されていること
  - E2EテストT01〜T17が全て実装・pass していること
  - データ制約（貸出中削除不可・最後の管理者削除不可・貸出中借用者削除不可）が実装されていること
  - セキュリティ要件（JWT認証・bcryptハッシュ・認可）が実装されていること
  - docker compose でシステムが正常起動すること
- **バリデーション**: E2Eテスト全17件が `docker compose run --rm -e BASE_URL=http://frontend test_playwright sh -c "npm install && npx playwright test"` で pass すること
