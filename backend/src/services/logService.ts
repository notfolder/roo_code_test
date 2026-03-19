import { PoolClient } from "pg";

// 操作ログ追加専用サービス
export class LogService {
  private client: PoolClient;

  constructor(client: PoolClient) {
    this.client = client;
  }

  async add(actorUserId: number | null, action: string, targetType: string, targetId: number | null, detail: string) {
    await this.client.query(
      `INSERT INTO operation_logs (actor_user_id, action, target_type, target_id, detail, created_at)
       VALUES ($1,$2,$3,$4,$5, now())`,
      [actorUserId, action, targetType, targetId, detail]
    );
  }
}
