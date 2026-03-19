// 初期管理者ユーザーを1件投入するスクリプト
// パスワード: AdminPass123

const { Pool } = require("pg");
const bcrypt = require("bcryptjs");
require("dotenv").config({ path: "../.env" });

async function main() {
  const pool = new Pool({ connectionString: process.env.DATABASE_URL });
  const client = await pool.connect();
  try {
    const hash = await bcrypt.hash("AdminPass123", 10);
    const sql = `
      INSERT INTO users (login_id, name, role, password_hash, password_expires_at, is_locked, created_at, updated_at)
      VALUES ($1,$2,$3,$4, now() + interval '90 days', false, now(), now())
      ON CONFLICT (login_id) DO NOTHING;
    `;
    await client.query(sql, ["admin", "管理者", "admin", hash]);
    console.log("Seed admin inserted (login_id=admin)");
  } finally {
    client.release();
    await pool.end();
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
