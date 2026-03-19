import iconv from "iconv-lite";
import { stringify } from "csv-stringify/sync";
import { PoolClient } from "pg";
import { Errors } from "../utils/errors";

// CSV 出力サービス
export class CsvExportService {
  private client: PoolClient;

  constructor(client: PoolClient) {
    this.client = client;
  }

  async exportReservations(filter: { from: Date; to: Date; equipmentId?: number; userId?: number }) {
    if (!filter.from || !filter.to) {
      throw Errors.validation("期間指定は必須です");
    }
    const cond: string[] = ["r.start_at >= $1", "r.end_at <= $2"];
    const params: any[] = [filter.from, filter.to];
    if (filter.equipmentId) {
      params.push(filter.equipmentId);
      cond.push(`r.equipment_id = $${params.length}`);
    }
    if (filter.userId) {
      params.push(filter.userId);
      cond.push(`r.user_id = $${params.length}`);
    }
    const sql = `
      SELECT e.management_number, e.name AS equipment_name, e.category, e.location,
             u.login_id AS user_login, r.start_at, r.end_at, r.status
      FROM reservations r
      JOIN equipment e ON e.id = r.equipment_id
      JOIN users u ON u.id = r.user_id
      WHERE ${cond.join(" AND ")}
      ORDER BY r.start_at
    `;
    const res = await this.client.query(sql, params);
    const records = res.rows.map((row) => [
      row.management_number,
      row.equipment_name,
      row.category,
      row.location,
      row.user_login,
      row.start_at,
      row.end_at,
      row.status,
    ]);
    const csv = stringify(records, {
      header: true,
      columns: [
        "管理番号",
        "名称",
        "カテゴリ",
        "設置場所",
        "予約者",
        "開始日時",
        "終了日時",
        "状態",
      ],
      record_delimiter: "\r\n",
    });
    const safe = csv
      .split("\r\n")
      .map((line) => {
        if (/^[=+\-@\t]/.test(line)) return "'" + line;
        return line;
      })
      .join("\r\n");
    const sjis = iconv.encode(safe, "Shift_JIS");
    return sjis;
  }
}
