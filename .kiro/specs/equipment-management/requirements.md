# 要件定義書

## はじめに

本ドキュメントは「備品管理・貸出管理アプリ」の要件を定義します。
オフィス用品・機器などの備品を一元管理し、社員が備品を借りる・返却するフローを効率化することを目的とします。

---

## 用語集

- **System**: 備品管理・貸出管理アプリ全体
- **Equipment**: 管理対象の備品（オフィス用品、PC、プロジェクターなど）
- **Equipment_Registry**: 備品の登録・更新・削除を担うモジュール
- **Loan_Manager**: 貸出・返却処理を担うモジュール
- **Search_Engine**: 備品の検索・フィルタリングを担うモジュール
- **Notification_Service**: 通知を送信するモジュール
- **User**: システムを利用する社員
- **Admin**: 備品の登録・管理権限を持つ管理者
- **Loan_Record**: 貸出の記録（貸出日、返却予定日、返却日、貸出者情報を含む）
- **Equipment_Status**: 備品の現在の状態（利用可能 / 貸出中 / メンテナンス中 / 廃棄済み）

---

## 要件

### 要件 1: 備品の登録・管理

**ユーザーストーリー:** 管理者として、備品の情報を登録・編集・削除したい。そうすることで、社内の備品を一元的に把握できる。

#### 受け入れ基準

1. WHEN Admin が備品名・カテゴリ・数量・管理番号を入力して登録操作を行う, THE Equipment_Registry SHALL 備品情報をシステムに保存し、一意の管理IDを付与する
2. WHEN Admin が既存の備品情報を編集して保存操作を行う, THE Equipment_Registry SHALL 変更内容を反映し、更新日時を記録する
3. WHEN Admin が備品の削除操作を行う, THE Equipment_Registry SHALL 対象備品に「廃棄済み」ステータスを設定し、物理削除は行わない
4. IF 同一管理番号の備品がすでに存在する, THEN THE Equipment_Registry SHALL 重複エラーメッセージを返し、登録を中断する
5. THE Equipment_Registry SHALL 備品ごとに備品名・カテゴリ・数量・管理番号・Equipment_Status・登録日時・更新日時を保持する

---

### 要件 2: 備品の検索・一覧表示

**ユーザーストーリー:** ユーザーとして、備品を素早く検索・絞り込みたい。そうすることで、必要な備品が利用可能かどうかをすぐに確認できる。

#### 受け入れ基準

1. THE Search_Engine SHALL 全備品の一覧をページネーション付きで表示する（1ページあたり20件）
2. WHEN User がキーワードを入力して検索操作を行う, THE Search_Engine SHALL 備品名・カテゴリ・管理番号に対して部分一致検索を実行し、結果を返す
3. WHEN User がカテゴリまたは Equipment_Status でフィルタリング操作を行う, THE Search_Engine SHALL 条件に一致する備品のみを表示する
4. WHEN 検索条件に一致する備品が存在しない, THE Search_Engine SHALL 「該当する備品が見つかりません」というメッセージを表示する

---

### 要件 3: 備品の貸出申請

**ユーザーストーリー:** ユーザーとして、備品の貸出申請をしたい。そうすることで、必要な備品を一定期間使用できる。

#### 受け入れ基準

1. WHEN User が利用可能な備品に対して貸出申請を行う, THE Loan_Manager SHALL Loan_Record を作成し、対象備品の Equipment_Status を「貸出中」に変更する
2. IF 申請対象の備品の Equipment_Status が「貸出中」または「メンテナンス中」である, THEN THE Loan_Manager SHALL 貸出不可メッセージを返し、申請を中断する
3. WHEN User が貸出申請を行う, THE Loan_Manager SHALL 貸出日・返却予定日・貸出者のUser IDを Loan_Record に記録する
4. IF 返却予定日が貸出日より前の日付である, THEN THE Loan_Manager SHALL バリデーションエラーを返し、申請を中断する
5. THE Loan_Manager SHALL 1ユーザーあたり同時に最大5件までの貸出を許可する
6. IF User の現在の貸出件数が5件に達している, THEN THE Loan_Manager SHALL 上限超過エラーメッセージを返し、申請を中断する

---

### 要件 4: 備品の返却処理

**ユーザーストーリー:** ユーザーとして、借りた備品を返却したい。そうすることで、他のユーザーが備品を利用できるようになる。

#### 受け入れ基準

1. WHEN User が貸出中の備品に対して返却操作を行う, THE Loan_Manager SHALL Loan_Record に返却日時を記録し、対象備品の Equipment_Status を「利用可能」に変更する
2. IF 返却操作を行う User が当該 Loan_Record の貸出者でない, THEN THE Loan_Manager SHALL 権限エラーメッセージを返し、返却処理を中断する
3. WHEN 返却処理が完了する, THE Loan_Manager SHALL 返却完了の通知を Notification_Service に送信する

---

### 要件 5: 貸出履歴の確認

**ユーザーストーリー:** ユーザーおよび管理者として、貸出履歴を確認したい。そうすることで、備品の利用状況を把握できる。

#### 受け入れ基準

1. WHEN User が自分の貸出履歴を参照する, THE Loan_Manager SHALL 当該 User に紐づく全 Loan_Record を返却日時の降順で返す
2. WHEN Admin が特定の備品の貸出履歴を参照する, THE Loan_Manager SHALL 対象備品に紐づく全 Loan_Record を返却日時の降順で返す
3. THE Loan_Manager SHALL 各 Loan_Record に備品名・貸出日・返却予定日・返却日・貸出者名を含める

---

### 要件 6: 返却期限超過の通知

**ユーザーストーリー:** 管理者として、返却期限を超過した貸出を把握したい。そうすることで、備品の未返却を防止できる。

#### 受け入れ基準

1. WHEN 返却予定日を経過しても返却されていない Loan_Record が存在する, THE Notification_Service SHALL 貸出者の User に返却期限超過の通知を送信する
2. WHEN 返却予定日の1日前になる, THE Notification_Service SHALL 貸出者の User に返却期限が翌日である旨の通知を送信する
3. THE System SHALL 返却期限チェックを1日1回実行する

---

### 要件 7: 備品ステータスの管理

**ユーザーストーリー:** 管理者として、備品のステータスを手動で変更したい。そうすることで、メンテナンス中の備品が誤って貸し出されることを防げる。

#### 受け入れ基準

1. WHEN Admin が備品のステータスを「メンテナンス中」に変更する, THE Equipment_Registry SHALL Equipment_Status を更新し、更新日時を記録する
2. WHILE 備品の Equipment_Status が「貸出中」である, THE Equipment_Registry SHALL Admin によるステータス変更操作を受け付けない
3. IF Admin が「廃棄済み」ステータスの備品のステータス変更を試みる, THEN THE Equipment_Registry SHALL 変更不可エラーメッセージを返す
