import bcrypt from "bcryptjs";
import jwt from "jsonwebtoken";
import { PoolClient } from "pg";
import { config } from "../config";
import { Errors } from "../utils/errors";
import { validatePasswordPolicy } from "../utils/passwordPolicy";
import { UserRepository } from "../repositories/userRepository";
import { withTransaction } from "../db";

// 認証とパスワード管理を担うサービス
export class AuthService {
  // ログインし、JWT を返却
  async login(loginId: string, password: string) {
    return await withTransaction(async (client: PoolClient) => {
      const repo = new UserRepository(client);
      const user = await repo.findByLoginId(loginId);
      if (!user || user.deletedAt) throw Errors.authInvalid();
      if (user.isLocked) throw Errors.authInvalid();
      const ok = await bcrypt.compare(password, user.passwordHash);
      if (!ok) throw Errors.authInvalid();
      if (user.passwordExpiresAt.getTime() < Date.now()) {
        throw Errors.authExpired();
      }
      const token = jwt.sign({ userId: user.id, role: user.role }, config.jwtSecret, {
        expiresIn: "12h",
      });
      return { token, user: { id: user.id, name: user.name, role: user.role } };
    });
  }

  // パスワード初期化（管理者用）
  async resetPassword(userId: number, tempPassword: string) {
    if (!validatePasswordPolicy(tempPassword)) {
      throw Errors.validation("パスワードポリシーに違反しています");
    }
    const hash = await bcrypt.hash(tempPassword, 10);
    const expires = new Date();
    expires.setDate(expires.getDate() + config.passwordExpireDays);
    await withTransaction(async (client: PoolClient) => {
      const repo = new UserRepository(client);
      await repo.updatePassword(userId, hash, expires);
      await repo.setLock(userId, false);
    });
  }
}
