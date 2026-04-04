# タスクリスト: 備品管理・貸出管理アプリ

## 実装タスク

### フェーズ 1: 基盤構築

- [ ] 1.1 プロジェクトセットアップ
  - [x] 1.1.1 バックエンド（Node.js / TypeScript）プロジェクト初期化
  - [x] 1.1.2 フロントエンド（React / TypeScript）プロジェクト初期化
  - [x] 1.1.3 データベース（PostgreSQL）セットアップ・マイグレーション基盤構築
  - [x] 1.1.4 Docker Compose による開発環境構築

- [ ] 1.2 認証基盤（JWT）
  - [x] 1.2.1 ユーザーモデル（id / name / email / role）の実装
  - [x] 1.2.2 ログインエンドポイント（POST `/auth/login`）の実装
  - [x] 1.2.3 JWT 発行・検証ミドルウェアの実装
  - [x] 1.2.4 ロールガード（USER / ADMIN）の実装
  - [x] 1.2.5 認証・認可の単体テスト

---

### フェーズ 2: Equipment Registry（備品管理）

- [ ] 2.1 データモデル実装
  - [x] 2.1.1 `Equipment` テーブル定義（id / assetNumber / name / category / quantity / status / createdAt / updatedAt）
  - [x] 2.1.2 `EquipmentStatus` 列挙型（AVAILABLE / ON_LOAN / DISPOSED）の定義

- [ ] 2.2 備品 CRUD API
  - [x] 2.2.1 備品登録（POST `/equipments`）— ADMIN のみ
    - 管理番号重複チェック（要件 1-4）
    - 一意の管理 ID 付与（要件 1-1）
  - [x] 2.2.2 備品一覧取得（GET `/equipments`）— USER / ADMIN
    - ページネーション（1ページ20件）（要件 2-1）
  - [x] 2.2.3 備品詳細取得（GET `/equipments/{id}`）— USER / ADMIN
  - [x] 2.2.4 備品情報更新（PUT `/equipments/{id}`）— ADMIN のみ
    - 更新日時の記録（要件 1-2）
  - [x] 2.2.5 備品廃棄（DELETE `/equipments/{id}`）— ADMIN のみ
    - 論理削除（ステータスを DISPOSED に変更）（要件 1-3）
    - 貸出中の備品は廃棄不可（ステータス遷移制約）

- [x] 2.3 Equipment Registry 単体テスト・統合テスト

---

### フェーズ 3: Search Engine（検索）

- [ ] 3.1 検索 API
  - [x] 3.1.1 キーワード検索（GET `/equipments/search?q=...`）— USER / ADMIN
    - 備品名・カテゴリ・管理番号の部分一致（要件 2-2）
  - [x] 3.1.2 カテゴリ・ステータスフィルタリング（`category` / `status` クエリパラメータ）（要件 2-3）
  - [x] 3.1.3 検索結果ゼロ件時のメッセージ返却（要件 2-4）
  - [x] 3.1.4 ページネーション対応（`page` / `size` クエリパラメータ）

- [x] 3.2 Search Engine 単体テスト・統合テスト

---

### フェーズ 4: Loan Manager（貸出・返却管理）

- [ ] 4.1 データモデル実装
  - [x] 4.1.1 `LoanRecord` テーブル定義（id / equipmentId / userId / loanDate / dueDate / returnedAt / createdAt）

- [ ] 4.2 貸出登録 API（POST `/loans`）— ADMIN のみ
  - [x] 4.2.1 貸出対象備品のステータスチェック（AVAILABLE のみ許可）（要件 3-2）
  - [x] 4.2.2 LoanRecord 作成・備品ステータスを ON_LOAN に変更（要件 3-1）
  - [x] 4.2.3 貸出日・返却予定日・貸出者 User ID の記録（要件 3-3）
  - [x] 4.2.4 返却予定日バリデーション（貸出日より後であること）（要件 3-4）
  - [x] 4.2.5 同時貸出上限チェック（1ユーザー最大5件）（要件 3-5, 3-6）

- [ ] 4.3 返却登録 API（POST `/loans/{id}/return`）— ADMIN のみ
  - [x] 4.3.1 返却日時の記録・備品ステータスを AVAILABLE に変更（要件 4-1）
  - [x] 4.3.2 返却完了後に Notification_Service へ通知送信（要件 4-3）

- [ ] 4.4 貸出履歴参照 API
  - [x] 4.4.1 ユーザー別貸出履歴（GET `/loans/user/{userId}`）— USER / ADMIN（要件 5-1）
  - [x] 4.4.2 備品別貸出履歴（GET `/loans/equipment/{equipmentId}`）— ADMIN のみ（要件 5-2）
  - [x] 4.4.3 各 LoanRecord に備品名・貸出日・返却予定日・返却日・貸出者名を含める（要件 5-3）
  - [x] 4.4.4 返却日時の降順ソート（要件 5-1, 5-2）

- [x] 4.5 Loan Manager 単体テスト・統合テスト

---

### フェーズ 5: Notification Service & Scheduler（通知・バッチ）

- [ ] 5.1 Notification Service 実装
  - [x] 5.1.1 `sendReturnReminder(userId, loanRecord)` — 返却期限前日通知（要件 6-2）
  - [x] 5.1.2 `sendOverdueNotification(userId, loanRecord)` — 返却期限超過通知（要件 6-1）

- [ ] 5.2 Scheduler（日次バッチ）実装
  - [x] 5.2.1 毎日 AM 9:00 実行のスケジューラー設定（要件 6-3）
  - [x] 5.2.2 返却予定日が翌日の LoanRecord を取得 → 前日リマインダー送信（要件 6-2）
  - [x] 5.2.3 返却予定日超過かつ未返却の LoanRecord を取得 → 超過通知送信（要件 6-1）

- [x] 5.3 Notification Service・Scheduler 単体テスト

---

### フェーズ 6: Web UI

- [ ] 6.1 共通コンポーネント・レイアウト
  - [x] 6.1.1 ログイン画面
  - [x] 6.1.2 ナビゲーションバー（ロール別メニュー表示）
  - [x] 6.1.3 認証済みルートガード

- [ ] 6.2 備品一覧・検索画面（USER / ADMIN）
  - [x] 6.2.1 備品一覧表示（ページネーション付き）
  - [x] 6.2.2 キーワード検索フォーム
  - [x] 6.2.3 カテゴリ・ステータスフィルター
  - [x] 6.2.4 検索結果ゼロ件メッセージ表示

- [ ] 6.3 備品管理画面（ADMIN）
  - [x] 6.3.1 備品登録フォーム
  - [x] 6.3.2 備品編集フォーム
  - [x] 6.3.3 備品廃棄操作（確認ダイアログ付き）

- [ ] 6.4 貸出・返却管理画面（ADMIN）
  - [x] 6.4.1 貸出登録フォーム（備品選択・貸出先ユーザー・返却予定日）
  - [x] 6.4.2 返却登録操作

- [ ] 6.5 貸出履歴画面
  - [x] 6.5.1 自分の貸出履歴一覧（USER / ADMIN）
  - [x] 6.5.2 備品別貸出履歴一覧（ADMIN）

---

### フェーズ 7: 結合テスト・品質保証

- [ ] 7.1 API エンドツーエンドテスト（主要シナリオ）
  - [x] 7.1.1 備品登録 → 貸出 → 返却の正常フロー
  - [x] 7.1.2 重複管理番号・貸出上限・ステータス不正などのエラーシナリオ
- [x] 7.2 権限チェックテスト（USER が ADMIN 専用 API を呼び出した場合の 403 確認）
- [x] 7.3 Scheduler の動作確認テスト

