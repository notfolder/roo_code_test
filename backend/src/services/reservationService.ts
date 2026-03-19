import { PoolClient } from "pg";
import { Errors } from "../utils/errors";
import { assertReservationWindow, assertCancelable } from "../utils/time";
import { LogService } from "./logService";

// 予約・キャンセル・利用記録サービス
export class ReservationService {
  private client: PoolClient;
  private logService: LogService;

  constructor(client: PoolClient) {
    this.client = client;
    this.logService = new LogService(client);
  }

  async create(params: { equipmentId: number; userId: number; purpose: string; startAt: Date; endAt: Date }) {
    // 30分刻み/4時間/30日先の基本バリデーション
    assertReservationWindow(params.startAt, params.endAt);

    // 同一設備の重複予約を行ロックで確認
    const overlap = await this.client.query(
      `SELECT id FROM reservations
       WHERE equipment_id = $1
         AND status = 'reserved'
         AND start_at < $3 AND end_at > $2
       FOR UPDATE`,
      [params.equipmentId, params.startAt, params.endAt]
    );
    if ((overlap.rowCount ?? 0) > 0) throw Errors.doubleBooking();

    // 同一ユーザー同時2件制限
    const userActive = await this.client.query(
      `SELECT COUNT(*) AS cnt FROM reservations
       WHERE user_id = $1 AND status = 'reserved'
         AND end_at > NOW()`,
      [params.userId]
    );
    const cnt = parseInt(userActive.rows[0].cnt, 10);
    if (cnt >= 2) throw Errors.userLimit();

    // 備品ステータス確認
    const eq = await this.client.query(
      `SELECT status FROM equipment WHERE id = $1 AND deleted_at IS NULL`,
      [params.equipmentId]
    );
    if (eq.rowCount === 0) throw Errors.notFound("備品が存在しません");
    if (eq.rows[0].status !== "available") {
      throw Errors.validation("備品が利用不可の状態です");
    }

    // 予約登録
    const res = await this.client.query(
      `INSERT INTO reservations (equipment_id, user_id, purpose, start_at, end_at, status, created_at, updated_at)
       VALUES ($1,$2,$3,$4,$5,'reserved', now(), now())
       RETURNING id`,
      [params.equipmentId, params.userId, params.purpose, params.startAt, params.endAt]
    );
    const reservationId = res.rows[0].id as number;
    await this.logService.add(params.userId, "CREATE_RESERVATION", "reservation", reservationId, "予約作成");
    return reservationId;
  }

  async cancel(reservationId: number, userId: number) {
    const res = await this.client.query(
      `SELECT id, start_at, status FROM reservations WHERE id = $1 FOR UPDATE`,
      [reservationId]
    );
    if (res.rowCount === 0) throw Errors.notFound("予約が存在しません");
    const row = res.rows[0];
    if (row.status !== "reserved") throw Errors.validation("キャンセル可能な状態ではありません");
    assertCancelable(row.start_at);
    await this.client.query(
      `UPDATE reservations SET status = 'cancelled', cancelled_at = now(), updated_at = now() WHERE id = $1`,
      [reservationId]
    );
    await this.logService.add(userId, "CANCEL_RESERVATION", "reservation", reservationId, "予約キャンセル");
  }

  async recordUsage(reservationId: number, action: "start" | "end", actorUserId: number) {
    const res = await this.client.query(
      `SELECT id, status FROM reservations WHERE id = $1 FOR UPDATE`,
      [reservationId]
    );
    if (res.rowCount === 0) throw Errors.notFound("予約が存在しません");
    const row = res.rows[0];
    if (action === "start") {
      if (row.status !== "reserved") throw Errors.validation("開始記録できない状態です");
      await this.client.query(
        `UPDATE reservations SET usage_start_at = now(), updated_at = now() WHERE id = $1`,
        [reservationId]
      );
      await this.logService.add(actorUserId, "USAGE_START", "reservation", reservationId, "利用開始");
    } else {
      await this.client.query(
        `UPDATE reservations SET usage_end_at = now(), status = 'completed', updated_at = now() WHERE id = $1`,
        [reservationId]
      );
      await this.logService.add(actorUserId, "USAGE_END", "reservation", reservationId, "返却完了");
    }
  }

  async listOverdue() {
    const res = await this.client.query(
      `SELECT id, equipment_id, user_id, purpose, start_at, end_at, status, usage_end_at
       FROM reservations
       WHERE status = 'reserved' AND usage_end_at IS NULL AND end_at < NOW()`
    );
    return res.rows.map((r) => ({ ...r, overdue: true }));
  }

  async list(filter: { equipmentId?: number; from?: Date; to?: Date }) {
    const cond: string[] = [];
    const params: any[] = [];
    if (filter.equipmentId) {
      params.push(filter.equipmentId);
      cond.push(`equipment_id = $${params.length}`);
    }
    if (filter.from) {
      params.push(filter.from);
      cond.push(`end_at >= $${params.length}`);
    }
    if (filter.to) {
      params.push(filter.to);
      cond.push(`start_at <= $${params.length}`);
    }
    const where = cond.length ? `WHERE ${cond.join(" AND ")}` : "";
    const res = await this.client.query(
      `SELECT id, equipment_id, user_id, purpose, start_at, end_at, status, usage_start_at, usage_end_at, cancelled_at
       FROM reservations ${where}
       ORDER BY start_at`,
      params
    );
    return res.rows;
  }
}
