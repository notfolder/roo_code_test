# 備品管理・貸出管理システム 実装タスク一覧

## タスク一覧

---

### TASK-01: プロジェクト基盤構築（Docker環境）

**概要**: docker-compose.yml、各DockerfileおよびnginxのReverseProxy設定を作成する。

**作業内容**:
- docker-compose.yml を作成（frontend / backend / db の3サービス定義）
- backend/Dockerfile を作成（Python 3.12 + Uvicorn）
- frontend/Dockerfile を作成（マルチステージビルド: node→nginx）
- frontend/nginx.conf を作成（静的配信 + /api/ リバースプロキシ設定）
- .env ファイルを作成（SECRET_KEY, DATABASE_URL, POSTGRES_* の環境変数）

**完了条件**:
- `docker compose up --build` でfrontend / backend / db の全コンテナが起動すること
- http://localhost にブラウザでアクセスできること（Vue初期画面）
- http://localhost/api/ へのアクセスがbackendコンテナに転送されること

**バリデーションタスク**:
- `docker compose ps` で全サービスが Running 状態であることを確認する
- `curl http://localhost` でHTMLが返ることを確認する
- `curl http://localhost/api/docs` でFastAPIのSwagger UIが返ることを確認する

---

### TASK-02: データベース設計実装（ORMモデル・スキーマ作成）

**概要**: SQLAlchemyのORMモデルとPydanticスキーマを実装する。

**作業内容**:
- app/database.py に DatabaseManager を実装（engine・SessionLocal・create_all_tables・create_initial_data）
- app/models/user.py に UserModel を実装
- app/models/equipment.py に EquipmentModel を実装
- app/models/loan_record.py に LoanRecordModel を実装
- app/schemas/auth.py に LoginRequest, TokenResponse を実装
- app/schemas/user.py に UserCreate, UserResponse を実装
- app/schemas/equipment.py に EquipmentCreate, EquipmentUpdate, EquipmentResponse を実装
- app/schemas/loan_record.py に LoanCreate, LoanReturn, LoanResponse を実装

**完了条件**:
- バックエンドコンテナ起動時にusers / equipment / loan_records テーブルが自動作成されること
- 初期管理者ユーザー（login_id: admin）が自動作成されること
- 各モデルのカラム定義が詳細設計書のテーブル定義と一致していること

**バリデーションタスク**:
- PostgreSQLに接続し `\dt` で3テーブルが存在することを確認する
- usersテーブルにadminユーザーが1件存在することを確認する
- Pydanticスキーマのバリデーション（最大文字数・必須項目）が設計書と一致していることをpytestで確認する

---

### TASK-03: 共通依存関係実装

**概要**: FastAPIの依存性注入（DBセッション・認証・管理者チェック）をCommonDependenciesとして実装する。

**作業内容**:
- app/dependencies.py に以下を実装する
  - `get_db`: DBセッションをyieldで提供するジェネレーター
  - `get_current_user`: AuthorizationヘッダーのJWTトークンを検証し現在ユーザーを返す関数
  - `require_admin`: 現在ユーザーのroleが'admin'でない場合に403例外を発生させる関数

**完了条件**:
- 有効なBearerトークンを付けたリクエストでcurrent_userが取得できること
- トークンなし・無効トークンで401が返ること
- 一般社員トークンでrequire_admin使用エンドポイントに対して403が返ること

**バリデーションタスク**:
- 単体テストUT-01〜UT-05の前提となる認証処理が正常に動作するか確認する
- IT-05（トークンなし401）・IT-07（一般社員403）が期待通りであることをpytestで確認する

---

### TASK-04: 認証サービス・ルーター実装

**概要**: AuthServiceとauth_routerを実装する。

**作業内容**:
- app/repositories/base.py に BaseRepository（get_by_id, get_all, create, update, delete）を実装
- app/repositories/user.py に UserRepository（get_by_login_id, has_active_loans）を実装
- app/services/auth.py に AuthService（authenticate, create_token, verify_token, hash_password, verify_password）を実装
- app/routers/auth.py に POST /api/auth/login エンドポイントを実装

**完了条件**:
- POST /api/auth/login で正しい資格情報の場合にJWTトークンが返ること
- POST /api/auth/login で誤った資格情報の場合に401が返ること

**バリデーションタスク**:
- 単体テストUT-01〜UT-05がすべてpassすること
- 結合テストIT-01・IT-02がすべてpassすること

---

### TASK-05: 備品サービス・ルーター実装

**概要**: EquipmentService・EquipmentRepositoryとequipment_routerを実装する。

**作業内容**:
- app/repositories/equipment.py に EquipmentRepository（get_available, update_status）を実装
- app/services/equipment.py に EquipmentService（get_all_equipment, create_equipment, update_equipment, delete_equipment）を実装
- app/routers/equipment.py に以下のエンドポイントを実装
  - GET /api/equipment/
  - POST /api/equipment/
  - PUT /api/equipment/{id}
  - DELETE /api/equipment/{id}

**完了条件**:
- 備品の登録・更新・削除・一覧取得が正常に動作すること
- 管理番号の重複登録で409が返ること
- 貸出中備品の削除で409が返ること

**バリデーションタスク**:
- 単体テストUT-06〜UT-11がすべてpassすること
- 結合テストIT-03〜IT-12がすべてpassすること

---

### TASK-06: 貸出サービス・ルーター実装

**概要**: LoanService・LoanRecordRepositoryとloan_routerを実装する。

**作業内容**:
- app/repositories/loan_record.py に LoanRecordRepository（get_active_loans, get_active_loan_by_equipment, return_loan）を実装
- app/services/loan.py に LoanService（get_all_loans, create_loan, return_loan）を実装
  - create_loan: SELECT FOR UPDATEによる悲観的ロックを使用したトランザクション処理
  - return_loan: SELECT FOR UPDATEによる悲観的ロックを使用したトランザクション処理
- app/routers/loan.py に以下のエンドポイントを実装
  - GET /api/loans/
  - POST /api/loans/
  - PUT /api/loans/{id}/return

**完了条件**:
- 貸出登録時に備品ステータスが'loaned'に変わること
- 返却登録時に備品ステータスが'available'に戻ること
- 貸出中備品への二重貸出で409が返ること
- 返却済み記録への再返却で409が返ること

**バリデーションタスク**:
- 単体テストUT-12〜UT-17がすべてpassすること
- 結合テストIT-13〜IT-18がすべてpassすること

---

### TASK-07: ユーザーサービス・ルーター実装

**概要**: UserService・UserRepositoryとuser_routerを実装する。

**作業内容**:
- UserRepositoryのhas_active_loansメソッドを実装
- app/services/user.py に UserService（get_all_users, create_user, delete_user）を実装
- app/routers/user.py に以下のエンドポイントを実装
  - GET /api/users/
  - POST /api/users/
  - DELETE /api/users/{id}

**完了条件**:
- ユーザーの登録・削除・一覧取得が正常に動作すること
- ログインIDの重複登録で409が返ること
- 貸出中ユーザーの削除で409が返ること

**バリデーションタスク**:
- 単体テストUT-18〜UT-22がすべてpassすること
- 結合テストIT-19〜IT-24がすべてpassすること

---

### TASK-08: フロントエンド基盤構築

**概要**: Vue 3 + Vuetify 3 + Pinia + Vue Router + axiosの初期設定を行う。

**作業内容**:
- frontend/src/main.js に Vue・Vuetify・Pinia・Vue Routerを初期化する
- frontend/src/api/client.js に apiClient（axiosインスタンス）を実装する
  - ベースURL: /api
  - リクエストインターセプター: localStorageからJWTトークンを取得しAuthorizationヘッダーに付与
  - レスポンスインターセプター: 401エラー時にauthStoreをクリアしログイン画面へリダイレクト（ログインAPIへの401は除く）
- frontend/src/stores/auth.js に useAuthStore を実装
- frontend/src/router/index.js にナビゲーションガードを含む全ルートを定義

**完了条件**:
- 未認証状態でダッシュボードURL（/）にアクセスするとログイン画面へリダイレクトされること
- 認証済み状態でログインURL（/login）にアクセスするとダッシュボードへリダイレクトされること
- APIリクエストに自動でBearerトークンが付与されること

**バリデーションタスク**:
- システムテストST-01・ST-02・ST-05をブラウザで実施し確認する

---

### TASK-09: ログイン画面（S1）実装

**概要**: LoginView.vue を実装する。

**作業内容**:
- Vuetifyを使用してS1のモックアップ通りのレイアウトを実装する
- useAuthStoreのログインアクションを呼び出す
- ログイン成功時はダッシュボード画面（/）へ遷移する
- 認証失敗時はエラーメッセージを画面に表示する

**完了条件**:
- 正しい資格情報でログインするとダッシュボード画面に遷移すること
- 誤った資格情報でエラーメッセージが表示されること

**バリデーションタスク**:
- システムテストST-03（管理者ログイン）・ST-04（一般社員ログイン）をブラウザで実施し確認する

---

### TASK-10: 貸出状況一覧画面（S2）実装

**概要**: DashboardView.vue を実装する。

**作業内容**:
- 全備品の貸出状況をuseLoanStore・useEquipmentStoreを使用して表示する
- 管理者の場合のみ操作ボタン（貸出登録・返却登録・備品管理・ユーザー管理）を表示する
- ログアウトボタンによりauthStoreをクリアしログイン画面へ遷移する

**完了条件**:
- 貸出状況一覧が正しく表示されること
- 管理者には操作ボタンが表示され、一般社員には表示されないこと
- ログアウト後にブラウザバックしてもダッシュボードが表示されないこと

**バリデーションタスク**:
- システムテストST-03・ST-04・ST-10・ST-14をブラウザで実施し確認する

---

### TASK-11: 貸出登録画面（S3）実装

**概要**: LoanCreateView.vue を実装する。

**作業内容**:
- 貸出可能な備品一覧（ドロップダウン）、ユーザー一覧（ドロップダウン）、貸出日（日付入力）を実装する
- useLoanStoreのcreate_loanアクションを呼び出す
- 登録成功時はダッシュボード画面へ遷移する
- エラー時はスナックバーでメッセージを表示する

**完了条件**:
- 貸出登録が正常に完了しダッシュボードで「貸出中」状態が確認できること
- 備品ドロップダウンに貸出可能な備品のみ表示されること

**バリデーションタスク**:
- システムテストST-09をブラウザで実施し確認する

---

### TASK-12: 返却登録画面（S4）実装

**概要**: ReturnCreateView.vue を実装する。

**作業内容**:
- 貸出中の記録一覧（備品名・借用者・貸出日）と返却日入力を実装する
- useLoanStoreのreturn_loanアクションを呼び出す
- 登録成功時はダッシュボード画面へ遷移する

**完了条件**:
- 返却登録が正常に完了しダッシュボードで「貸出可」状態に戻ることが確認できること

**バリデーションタスク**:
- システムテストST-11をブラウザで実施し確認する

---

### TASK-13: 備品管理画面（S5・S6）実装

**概要**: EquipmentListView.vue と EquipmentFormView.vue を実装する。

**作業内容**:
- 備品一覧表示（管理番号・品名・状態・編集ボタン・削除ボタン）を実装する
- 貸出中の備品は削除ボタンを非活性にする
- 新規登録・編集フォームを実装する
- 編集時は管理番号フィールドを読み取り専用（変更不可）にする

**完了条件**:
- 備品登録・編集が正常に動作すること
- 貸出中の備品の削除ボタンが非活性であること

**バリデーションタスク**:
- システムテストST-06・ST-07・ST-12をブラウザで実施し確認する

---

### TASK-14: ユーザー管理画面（S7・S8）実装

**概要**: UserListView.vue と UserFormView.vue を実装する。

**作業内容**:
- ユーザー一覧表示（氏名・ログインID・役割・削除ボタン）を実装する
- 貸出中の借用者は削除ボタンを非活性にする
- ユーザー登録フォームを実装する

**完了条件**:
- ユーザー登録・削除が正常に動作すること
- 貸出中ユーザーの削除ボタンが非活性であること

**バリデーションタスク**:
- システムテストST-08・ST-13をブラウザで実施し確認する

---

### TASK-15: バックエンド単体テスト実装

**概要**: tests/unit/backend/ 以下の全単体テストを実装する。

**作業内容**:
- test_auth_service.py: UT-01〜UT-05
- test_equipment_service.py: UT-06〜UT-11
- test_loan_service.py: UT-12〜UT-17
- test_user_service.py: UT-18〜UT-22

**完了条件**:
- `pytest tests/unit/` で全22ケースがpassすること

**バリデーションタスク**:
- `pytest tests/unit/ -v` の出力で全テストケースIDと結果を確認する

---

### TASK-16: バックエンド結合テスト実装

**概要**: tests/integration/backend/ 以下の全結合テストを実装する。

**作業内容**:
- test_auth_api.py: IT-01〜IT-02
- test_equipment_api.py: IT-03〜IT-12
- test_loan_api.py: IT-13〜IT-18
- test_user_api.py: IT-19〜IT-24

**完了条件**:
- `pytest tests/integration/` で全24ケースがpassすること

**バリデーションタスク**:
- `pytest tests/integration/ -v` の出力で全テストケースIDと結果を確認する

---

### TASK-17: README.md 作成

**概要**: 起動方法・操作説明を記載したREADME.mdをプロジェクトルートに作成する。

**作業内容**:
- 前提条件（Docker・Docker Compose のインストール要件）
- 起動コマンド（`docker compose up --build`）
- アクセスURL（`http://localhost`）
- 初期管理者ユーザーの認証情報（login_id: admin、パスワード: admin1234）
- 初期パスワードの変更手順（ユーザー削除・再登録）
- 停止コマンド（`docker compose down`）
- データ永続化の説明（Dockerボリューム）

**完了条件**:
- README.mdの手順通りにコマンドを実行しシステムが起動すること
- ドキュメントの内容が実装と一致していること

**バリデーションタスク**:
- README.mdのコマンドをそのまま実行してシステムが正常起動することを確認する

---

### TASK-18: 全変更点実装確認

**概要**: 詳細設計書と実装内容を照合し、すべての設計が実装されていることを確認する。

**作業内容**:
- 詳細設計書のエンドポイント一覧と実装を照合する
- 詳細設計書の画面一覧（S1〜S8）と実装を照合する
- 詳細設計書のクラス一覧と実装を照合する
- テスト設計書の全テストケース（UT/IT/ST）が実装・実施済みであることを確認する

**完了条件**:
- 設計書に記載された全エンドポイント・全画面・全クラスが実装されていること
- `pytest tests/` で全単体・結合テストがpassすること
- システムテストST-01〜ST-14が全て成功していること
- `docker compose up --build` でシステムが正常起動すること

**バリデーションタスク**:
- 上記全チェックを実施し、差分がないことを最終確認する
