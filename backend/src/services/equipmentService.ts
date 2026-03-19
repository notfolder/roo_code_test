import { PoolClient } from "pg";
import { EquipmentStatus } from "../models/types";
import { Errors } from "../utils/errors";

// 備品の取得・状態変更サービス
export class EquipmentService {
  private client: PoolClient;

  constructor(client: PoolClient) {
    this.client = client;
  }

  // フィルタ付き一覧取得
  async list(filter: { category?: string; location?: string; status?: EquipmentStatus; q?: string }) {
    const cond: string[] = ["deleted_at IS NULL"];
    const params: any[] = [];
    if (filter.category) {
      params.push(filter.category);
      cond.push(`category = $${params.length}`);
    }
    if (filter.location) {
      params.push(filter.location);
      cond.push(`location = $${params.length}`);
    }
    if (filter.status) {
      params.push(filter.status);
      cond.push(`status = $${params.length}`);
    }
    if (filter.q) {
      params.push(`%${filter.q}%`);
      cond.push(`(name ILIKE $${params.length} OR description ILIKE $${params.length})`);
    }

    const sql = `SELECT id, management_number, name, category, location, status, description, created_at, updated_at, deleted_at
                 FROM equipment
                 WHERE ${cond.join(" AND ")}
                 ORDER BY management_number`;
    const res = await this.client.query(sql, params);
    return res.rows;
  }

  // 状態変更
  async updateStatus(equipmentId: number, status: EquipmentStatus) {
    const res = await this.client.query(
      `UPDATE equipment SET status = $1, updated_at = now() WHERE id = $2 AND deleted_at IS NULL RETURNING id`,
      [status, equipmentId]
    );
    if (res.rowCount === 0) throw Errors.notFound("備品が存在しません");
  }
}
