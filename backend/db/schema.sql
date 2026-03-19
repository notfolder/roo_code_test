-- データベース初期スキーマ
-- 要件: PostgreSQL / 予約重複はアプリ側でトランザクション制御

-- タイムスタンプ自動更新トリガー
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- users テーブル
CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  login_id VARCHAR(64) NOT NULL UNIQUE,
  name VARCHAR(100) NOT NULL,
  role VARCHAR(10) NOT NULL CHECK (role IN ('admin','user')),
  password_hash VARCHAR(255) NOT NULL,
  password_expires_at TIMESTAMP NOT NULL,
  is_locked BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
  deleted_at TIMESTAMP NULL
);

DROP TRIGGER IF EXISTS trg_users_updated_at ON users;
CREATE TRIGGER trg_users_updated_at
BEFORE UPDATE ON users
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

-- equipment テーブル
CREATE TABLE IF NOT EXISTS equipment (
  id SERIAL PRIMARY KEY,
  management_number VARCHAR(50) NOT NULL UNIQUE,
  name VARCHAR(150) NOT NULL,
  category VARCHAR(50) NOT NULL,
  location VARCHAR(100) NOT NULL,
  status VARCHAR(15) NOT NULL CHECK (status IN ('available','broken','maintenance')),
  description TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
  deleted_at TIMESTAMP NULL
);

DROP TRIGGER IF EXISTS trg_equipment_updated_at ON equipment;
CREATE TRIGGER trg_equipment_updated_at
BEFORE UPDATE ON equipment
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

-- reservations テーブル
CREATE TABLE IF NOT EXISTS reservations (
  id SERIAL PRIMARY KEY,
  equipment_id INTEGER NOT NULL REFERENCES equipment(id),
  user_id INTEGER NOT NULL REFERENCES users(id),
  purpose VARCHAR(200) NOT NULL,
  start_at TIMESTAMP NOT NULL,
  end_at TIMESTAMP NOT NULL,
  status VARCHAR(15) NOT NULL CHECK (status IN ('reserved','cancelled','completed')),
  cancelled_at TIMESTAMP NULL,
  usage_start_at TIMESTAMP NULL,
  usage_end_at TIMESTAMP NULL,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
  CONSTRAINT chk_reservation_time CHECK (end_at > start_at),
  CONSTRAINT chk_reservation_duration CHECK (end_at - start_at <= INTERVAL '4 hours'),
  CONSTRAINT chk_reservation_minutes CHECK (
    EXTRACT(MINUTE FROM start_at)::int % 30 = 0 AND
    EXTRACT(MINUTE FROM end_at)::int % 30 = 0
  )
);

DROP TRIGGER IF EXISTS trg_reservations_updated_at ON reservations;
CREATE TRIGGER trg_reservations_updated_at
BEFORE UPDATE ON reservations
FOR EACH ROW EXECUTE FUNCTION set_updated_at();

-- operation_logs テーブル
CREATE TABLE IF NOT EXISTS operation_logs (
  id SERIAL PRIMARY KEY,
  actor_user_id INTEGER NULL REFERENCES users(id),
  action VARCHAR(50) NOT NULL,
  target_type VARCHAR(30) NOT NULL,
  target_id INTEGER NULL,
  detail TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- インデックス
CREATE INDEX IF NOT EXISTS idx_reservations_equipment_time ON reservations(equipment_id, start_at, end_at);
CREATE INDEX IF NOT EXISTS idx_reservations_user_time ON reservations(user_id, start_at, end_at);
CREATE INDEX IF NOT EXISTS idx_operation_logs_actor_time ON operation_logs(actor_user_id, created_at);

-- 初期管理者を投入する場合の例（任意でコメント解除）
-- INSERT INTO users(login_id, name, role, password_hash, password_expires_at, is_locked)
-- VALUES ('admin', '管理者', 'admin', '<bcrypt-hash>', NOW() + INTERVAL '90 days', false);
