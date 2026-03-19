import { Pool, PoolClient } from "pg";
import fs from "fs";
import path from "path";
import { config } from "./config";

// PostgreSQL 接続プールの生成
export const pool = new Pool({ connectionString: config.databaseUrl });

// スキーマを初期化する（起動時に実行）
export async function ensureSchema(): Promise<void> {
  const client = await pool.connect();
  try {
    const schemaPath = path.resolve(__dirname, "../db/schema.sql");
    const sql = fs.readFileSync(schemaPath, "utf-8");
    await client.query(sql);
  } finally {
    client.release();
  }
}

// トランザクション実行ヘルパー
export async function withTransaction<T>(fn: (client: PoolClient) => Promise<T>): Promise<T> {
  const client = await pool.connect();
  try {
    await client.query("BEGIN");
    const result = await fn(client);
    await client.query("COMMIT");
    return result;
  } catch (error) {
    await client.query("ROLLBACK");
    throw error;
  } finally {
    client.release();
  }
}
