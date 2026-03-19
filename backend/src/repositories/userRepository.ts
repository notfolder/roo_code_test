import { PoolClient } from "pg";
import { User, UserRole } from "../models/types";

// ユーザーリポジトリ: DBアクセスを担当
export class UserRepository {
  private client: PoolClient;

  constructor(client: PoolClient) {
    this.client = client;
  }

  // loginId でユーザーを取得
  async findByLoginId(loginId: string): Promise<User | null> {
    const res = await this.client.query(
      `SELECT id, login_id, name, role, password_hash, password_expires_at, is_locked, created_at, updated_at, deleted_at
       FROM users WHERE login_id = $1 AND deleted_at IS NULL`,
      [loginId]
    );
    if (res.rowCount === 0) return null;
    const row = res.rows[0];
    return this.map(row);
  }

  // ユーザー作成
  async create(params: {
    loginId: string;
    name: string;
    role: UserRole;
    passwordHash: string;
    passwordExpiresAt: Date;
  }): Promise<User> {
    const res = await this.client.query(
      `INSERT INTO users (login_id, name, role, password_hash, password_expires_at, is_locked, created_at, updated_at)
       VALUES ($1,$2,$3,$4,$5,false,now(),now())
       RETURNING id, login_id, name, role, password_hash, password_expires_at, is_locked, created_at, updated_at, deleted_at`,
      [params.loginId, params.name, params.role, params.passwordHash, params.passwordExpiresAt]
    );
    return this.map(res.rows[0]);
  }

  // パスワード更新（期限リセット含む）
  async updatePassword(userId: number, passwordHash: string, expiresAt: Date): Promise<void> {
    await this.client.query(
      `UPDATE users SET password_hash = $1, password_expires_at = $2, updated_at = now() WHERE id = $3`,
      [passwordHash, expiresAt, userId]
    );
  }

  // ロック設定
  async setLock(userId: number, isLocked: boolean): Promise<void> {
    await this.client.query(
      `UPDATE users SET is_locked = $1, updated_at = now() WHERE id = $2`,
      [isLocked, userId]
    );
  }

  // ユーザーIDで取得
  async findById(userId: number): Promise<User | null> {
    const res = await this.client.query(
      `SELECT id, login_id, name, role, password_hash, password_expires_at, is_locked, created_at, updated_at, deleted_at
       FROM users WHERE id = $1 AND deleted_at IS NULL`,
      [userId]
    );
    if (res.rowCount === 0) return null;
    return this.map(res.rows[0]);
  }

  private map(row: any): User {
    return {
      id: row.id,
      loginId: row.login_id,
      name: row.name,
      role: row.role,
      passwordHash: row.password_hash,
      passwordExpiresAt: row.password_expires_at,
      isLocked: row.is_locked,
      createdAt: row.created_at,
      updatedAt: row.updated_at,
      deletedAt: row.deleted_at,
    };
  }
}
