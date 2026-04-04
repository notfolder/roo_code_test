# 実装タスク一覧：備品管理・貸出管理Webアプリ

## タスク一覧

### T-01 プロジェクト基盤構築
- [ ] docker-compose.yml を作成する（nginx / backend / db の3サービス）
- [ ] nginx/nginx.conf を作成する（静的ファイル配信 + /api/ プロキシ設定）
- [ ] backend/Dockerfile を作成する
- [ ] frontend/Dockerfile を作成する（マルチステージビルド）
- 完了条件：`docker compose up --build` でコンテナが全て起動すること

### T-02 バックエンド基盤
- [ ] requirements.txt を作成する（FastAPI, SQLAlchemy, psycopg2, python-jose, bcrypt, pydantic）
- [ ] database.py を作成する（DB接続・セッション管理）
- [ ] models/equipment.py を作成する（EquipmentModel）
- [ ] models/user.py を作成する（UserModel）
- [ ] init_db.py を作成する（スキーマ作成・初期ユーザー投入）
- [ ] main.py を作成する（FastAPIアプリ起動・ルーター登録・CORS設定）
- 完了条件：バックエンドコンテナ起動時にDBスキーマが自動作成され、初期ユーザーが投入されること

### T-03 バックエンド共通ユーティリティ
- [ ] utils/jwt_util.py を作成する（JWTUtil：トークン生成・検証）
- [ ] utils/password_util.py を作成する（PasswordUtil：bcryptハッシュ化・検証）
- [ ] utils/auth_guard.py を作成する（AuthGuard：依存性注入による認証・認可）
- 完了条件：単体テスト UT-01〜UT-06 が全て通ること

### T-04 バックエンド認証API
- [ ] schemas/user.py にログインリクエスト・レスポンスのPydanticスキーマを作成する
- [ ] services/auth_service.py を作成する（AuthService）
- [ ] routers/auth.py を作成する（AuthRouter：POST /api/auth/login）
- 完了条件：結合テスト IT-01、IT-02 が通ること

### T-05 バックエンド備品API
- [ ] schemas/equipment.py に備品リクエスト・レスポンスのPydanticスキーマを作成する
- [ ] repositories/equipment_repository.py を作成する（EquipmentRepository）
- [ ] services/equipment_service.py を作成する（EquipmentService）
- [ ] routers/equipment.py を作成する（EquipmentRouter：全備品エンドポイント）
- 完了条件：単体テスト UT-07〜UT-12 および結合テスト IT-03〜IT-13 が全て通ること

### T-06 バックエンドユーザーAPI
- [ ] repositories/user_repository.py を作成する（UserRepository）
- [ ] services/user_service.py を作成する（UserService）
- [ ] routers/user.py を作成する（UserRouter：全ユーザーエンドポイント）
- 完了条件：単体テスト UT-13、UT-14 および結合テスト IT-14〜IT-16 が全て通ること

### T-07 フロントエンド基盤
- [ ] package.json を作成する（Vue 3, Vuetify 3, Vue Router, Axios）
- [ ] vite.config.js を作成する
- [ ] src/main.js を作成する（Vueアプリ起動・Vuetify登録）
- [ ] src/api/client.js を作成する（apiClient：Axiosインスタンス・Authヘッダー付与・401インターセプト）
- [ ] src/router/index.js を作成する（Vue Router・未認証ガード・adminガード）
- [ ] src/composables/useAuth.js を作成する（ログイン状態・ロール・トークン管理）
- 完了条件：フロントエンドコンテナがビルドされ、ブラウザでログイン画面が表示されること

### T-08 フロントエンド画面実装
- [ ] src/views/LoginView.vue を作成する（SC-01）
- [ ] src/views/EquipmentListView.vue を作成する（SC-02：ロール別UI制御含む）
- [ ] src/views/EquipmentFormView.vue を作成する（SC-03・SC-04共用）
- [ ] src/views/LendView.vue を作成する（SC-05）
- [ ] src/views/ReturnView.vue を作成する（SC-06）
- [ ] src/views/UserListView.vue を作成する（SC-07）
- [ ] src/views/UserFormView.vue を作成する（SC-08・SC-09共用）
- [ ] src/composables/useEquipment.js を作成する
- [ ] src/composables/useUser.js を作成する
- 完了条件：総合テスト ST-01〜ST-07 が全て通ること

### T-09 README.md作成
- [ ] README.md を作成する（概要・前提条件・起動方法・初期ログイン情報・操作説明）
- 完了条件：README.mdの手順通りに起動・操作できること

### T-10 最終確認
- [ ] 全単体テスト（UT-01〜UT-14）が通ることを確認する
- [ ] 全結合テスト（IT-01〜IT-16）が通ることを確認する
- [ ] 全総合テスト（ST-01〜ST-07）が通ることを確認する
- [ ] 要件定義書の全機能（F-01〜F-12）が実装されていることを確認する
- [ ] 設計書の全APIエンドポイントが実装されていることを確認する
- 完了条件：全テストが通り、全機能・全APIが実装されていること
