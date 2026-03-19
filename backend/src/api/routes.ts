import express from "express";
import { withTransaction } from "../db";
import { AuthService } from "../services/authService";
import { ReservationService } from "../services/reservationService";
import { EquipmentService } from "../services/equipmentService";
import { CsvExportService } from "../services/csvExportService";
import { requireAuth, requireAdmin } from "../middleware/authMiddleware";
import { Errors } from "../utils/errors";

export const router = express.Router();

// 認証
router.post("/auth/login", async (req, res, next) => {
  try {
    const { login_id, password } = req.body;
    if (!login_id || !password) throw Errors.validation("login_id と password は必須です");
    const service = new AuthService();
    const result = await service.login(login_id, password);
    res.json(result);
  } catch (e) {
    next(e);
  }
});

// 備品一覧
router.get("/equipment", requireAuth, async (req, res, next) => {
  try {
    await withTransaction(async (client) => {
      const service = new EquipmentService(client);
      const list = await service.list({
        category: req.query.category as string | undefined,
        location: req.query.location as string | undefined,
        status: req.query.status as any,
        q: req.query.q as string | undefined,
      });
      res.json(list);
    });
  } catch (e) {
    next(e);
  }
});

// 備品ステータス変更（管理者）
router.put("/equipment/:id/status", requireAuth, requireAdmin, async (req, res, next) => {
  try {
    const status = req.body.status;
    await withTransaction(async (client) => {
      const service = new EquipmentService(client);
      await service.updateStatus(Number(req.params.id), status);
      res.json({ ok: true });
    });
  } catch (e) {
    next(e);
  }
});

// 予約作成
router.post("/reservations", requireAuth, async (req, res, next) => {
  try {
    const { equipment_id, purpose, start_at, end_at } = req.body;
    if (!equipment_id || !purpose || !start_at || !end_at) throw Errors.validation("必須項目が不足しています");
    await withTransaction(async (client) => {
      const service = new ReservationService(client);
      const id = await service.create({
        equipmentId: Number(equipment_id),
        userId: req.authUser!.userId,
        purpose,
        startAt: new Date(start_at),
        endAt: new Date(end_at),
      });
      res.json({ id });
    });
  } catch (e) {
    next(e);
  }
});

// 予約一覧/空き状況
router.get("/reservations", requireAuth, async (req, res, next) => {
  try {
    const equipmentId = req.query.equipment_id ? Number(req.query.equipment_id) : undefined;
    const from = req.query.from ? new Date(String(req.query.from)) : undefined;
    const to = req.query.to ? new Date(String(req.query.to)) : undefined;
    await withTransaction(async (client) => {
      const service = new ReservationService(client);
      const list = await service.list({ equipmentId, from, to });
      res.json(list);
    });
  } catch (e) {
    next(e);
  }
});

// キャンセル
router.post("/reservations/:id/cancel", requireAuth, async (req, res, next) => {
  try {
    await withTransaction(async (client) => {
      const service = new ReservationService(client);
      await service.cancel(Number(req.params.id), req.authUser!.userId);
      res.json({ ok: true });
    });
  } catch (e) {
    next(e);
  }
});

// 利用開始/終了
router.post("/reservations/:id/usage/start", requireAuth, async (req, res, next) => {
  try {
    await withTransaction(async (client) => {
      const service = new ReservationService(client);
      await service.recordUsage(Number(req.params.id), "start", req.authUser!.userId);
      res.json({ ok: true });
    });
  } catch (e) {
    next(e);
  }
});

router.post("/reservations/:id/usage/end", requireAuth, async (req, res, next) => {
  try {
    await withTransaction(async (client) => {
      const service = new ReservationService(client);
      await service.recordUsage(Number(req.params.id), "end", req.authUser!.userId);
      res.json({ ok: true });
    });
  } catch (e) {
    next(e);
  }
});

// 遅延一覧
router.get("/reservations/overdue", requireAuth, async (_req, res, next) => {
  try {
    await withTransaction(async (client) => {
      const service = new ReservationService(client);
      const list = await service.listOverdue();
      res.json(list);
    });
  } catch (e) {
    next(e);
  }
});

// CSV 出力（管理者）
router.get("/csv/reservations", requireAuth, requireAdmin, async (req, res, next) => {
  try {
    const from = req.query.from ? new Date(String(req.query.from)) : undefined;
    const to = req.query.to ? new Date(String(req.query.to)) : undefined;
    if (!from || !to) throw Errors.validation("期間指定は必須です");
    const equipmentId = req.query.equipment_id ? Number(req.query.equipment_id) : undefined;
    const userId = req.query.user_id ? Number(req.query.user_id) : undefined;
    await withTransaction(async (client) => {
      const service = new CsvExportService(client);
      const csv = await service.exportReservations({ from, to, equipmentId, userId });
      res.setHeader("Content-Type", "text/csv; charset=Shift_JIS");
      res.setHeader("Content-Disposition", "attachment; filename=reservations.csv");
      res.send(csv);
    });
  } catch (e) {
    next(e);
  }
});

// ヘルスチェック
router.get("/health", (_req, res) => res.json({ ok: true }));

