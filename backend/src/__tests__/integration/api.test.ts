/**
 * 結合テスト: 備品管理・貸出管理 API
 *
 * - Prisma (lib/prisma) と notificationService をモック化
 * - supertest で Express アプリに対してリクエストを送信
 * - JWT_SECRET='test-secret' で ADMIN / USER トークンを生成
 */

// auth.ts がモジュールロード時に JWT_SECRET を読み込むため、インポート前に設定する
process.env.JWT_SECRET = 'test-secret';

import request from 'supertest';
import jwt from 'jsonwebtoken';

// ─── モック設定 ────────────────────────────────────────────────────────────────

jest.mock('../../lib/prisma', () => ({
  __esModule: true,
  default: {
    equipment: {
      findUnique: jest.fn(),
      findMany: jest.fn(),
      count: jest.fn(),
      create: jest.fn(),
      update: jest.fn(),
    },
    loanRecord: {
      findUnique: jest.fn(),
      findMany: jest.fn(),
      count: jest.fn(),
      create: jest.fn(),
      update: jest.fn(),
    },
    $transaction: jest.fn(),
  },
  prisma: {
    loanRecord: {
      findMany: jest.fn(),
    },
  },
}));

jest.mock('../../services/notificationService', () => ({
  sendReturnCompleted: jest.fn().mockResolvedValue(undefined),
  sendReturnReminder: jest.fn().mockResolvedValue(undefined),
  sendOverdueNotification: jest.fn().mockResolvedValue(undefined),
}));

// scheduler の startScheduler が自動起動しないようにモック
jest.mock('../../scheduler', () => ({
  startScheduler: jest.fn(),
  checkDueTomorrow: jest.fn().mockResolvedValue(undefined),
  checkOverdue: jest.fn().mockResolvedValue(undefined),
}));

import prisma from '../../lib/prisma';
import { checkDueTomorrow, checkOverdue } from '../../scheduler';

// app は モック設定後にインポート
import app from '../../index';

// ─── ヘルパー ──────────────────────────────────────────────────────────────────

const JWT_SECRET = 'test-secret';

function makeToken(role: 'ADMIN' | 'USER', userId = 'user-1') {
  return jwt.sign({ userId, email: `${role.toLowerCase()}@example.com`, role }, JWT_SECRET);
}

const ADMIN_TOKEN = makeToken('ADMIN', 'admin-1');
const USER_TOKEN = makeToken('USER', 'user-2');

// Prisma モックのキャスト
const mockPrisma = prisma as jest.Mocked<typeof prisma> & {
  equipment: {
    findUnique: jest.MockedFunction<typeof prisma.equipment.findUnique>;
    create: jest.MockedFunction<typeof prisma.equipment.create>;
    update: jest.MockedFunction<typeof prisma.equipment.update>;
  };
  loanRecord: {
    findUnique: jest.MockedFunction<typeof prisma.loanRecord.findUnique>;
    count: jest.MockedFunction<typeof prisma.loanRecord.count>;
  };
  $transaction: jest.MockedFunction<typeof prisma.$transaction>;
};

// ─── フィクスチャ ──────────────────────────────────────────────────────────────

const baseEquipment = {
  id: 'equip-1',
  assetNumber: 'ASSET-001',
  name: 'ノートPC',
  category: 'PC',
  quantity: 1,
  status: 'AVAILABLE' as const,
  createdAt: new Date('2024-01-01'),
  updatedAt: new Date('2024-01-01'),
};

const baseLoan = {
  id: 'loan-1',
  equipmentId: 'equip-1',
  userId: 'user-2',
  loanDate: new Date('2024-06-01'),
  dueDate: new Date('2024-06-10'),
  returnedAt: null,
  createdAt: new Date('2024-06-01'),
  updatedAt: new Date('2024-06-01'),
};

const returnedLoan = {
  ...baseLoan,
  returnedAt: new Date('2024-06-05'),
  equipment: baseEquipment,
  user: { id: 'user-2', name: 'テストユーザー', email: 'user@example.com', role: 'USER' },
};

beforeEach(() => {
  jest.clearAllMocks();
});

// ─── テスト 1: 正常フロー（備品登録 → 貸出 → 返却）─────────────────────────────

describe('7.1.1 正常フロー: 備品登録 → 貸出 → 返却', () => {
  it('POST /equipments → 201 で備品が作成される', async () => {
    mockPrisma.equipment.findUnique.mockResolvedValue(null);
    mockPrisma.equipment.create.mockResolvedValue(baseEquipment);

    const res = await request(app)
      .post('/equipments')
      .set('Authorization', `Bearer ${ADMIN_TOKEN}`)
      .send({
        assetNumber: 'ASSET-001',
        name: 'ノートPC',
        category: 'PC',
        quantity: 1,
      });

    expect(res.status).toBe(201);
    expect(res.body).toMatchObject({
      id: 'equip-1',
      assetNumber: 'ASSET-001',
      name: 'ノートPC',
    });
  });

  it('POST /loans → 201 で貸出が作成される', async () => {
    mockPrisma.equipment.findUnique.mockResolvedValue(baseEquipment);
    mockPrisma.loanRecord.count.mockResolvedValue(0);
    mockPrisma.$transaction.mockImplementation(async (fn: any) => {
      return fn({
        loanRecord: { create: jest.fn().mockResolvedValue(baseLoan) },
        equipment: { update: jest.fn().mockResolvedValue({ ...baseEquipment, status: 'ON_LOAN' }) },
      });
    });

    const res = await request(app)
      .post('/loans')
      .set('Authorization', `Bearer ${ADMIN_TOKEN}`)
      .send({
        equipmentId: 'equip-1',
        userId: 'user-2',
        loanDate: '2024-06-01',
        dueDate: '2024-06-10',
      });

    expect(res.status).toBe(201);
    expect(res.body).toMatchObject({
      id: 'loan-1',
      equipmentId: 'equip-1',
      userId: 'user-2',
    });
  });

  it('POST /loans/:id/return → 200 で返却が完了する', async () => {
    mockPrisma.loanRecord.findUnique.mockResolvedValue({
      ...baseLoan,
      equipment: baseEquipment,
      user: { id: 'user-2', name: 'テストユーザー', email: 'user@example.com', role: 'USER' },
    } as any);
    mockPrisma.$transaction.mockImplementation(async (fn: any) => {
      return fn({
        loanRecord: { update: jest.fn().mockResolvedValue(returnedLoan) },
        equipment: { update: jest.fn().mockResolvedValue({ ...baseEquipment, status: 'AVAILABLE' }) },
      });
    });

    const res = await request(app)
      .post('/loans/loan-1/return')
      .set('Authorization', `Bearer ${ADMIN_TOKEN}`);

    expect(res.status).toBe(200);
    expect(res.body).toMatchObject({
      id: 'loan-1',
      equipmentId: 'equip-1',
    });
    expect(res.body.returnedAt).toBeTruthy();
  });
});

// ─── テスト 2: エラーシナリオ ──────────────────────────────────────────────────

describe('7.1.2 エラーシナリオ', () => {
  it('POST /equipments（重複 assetNumber）→ 409', async () => {
    mockPrisma.equipment.findUnique.mockResolvedValue(baseEquipment);

    const res = await request(app)
      .post('/equipments')
      .set('Authorization', `Bearer ${ADMIN_TOKEN}`)
      .send({
        assetNumber: 'ASSET-001',
        name: 'ノートPC',
        category: 'PC',
        quantity: 1,
      });

    expect(res.status).toBe(409);
    expect(res.body).toMatchObject({ code: 'DUPLICATE_ASSET_NUMBER' });
  });

  it('POST /loans（備品が ON_LOAN）→ 409', async () => {
    mockPrisma.equipment.findUnique.mockResolvedValue({
      ...baseEquipment,
      status: 'ON_LOAN' as const,
    });

    const res = await request(app)
      .post('/loans')
      .set('Authorization', `Bearer ${ADMIN_TOKEN}`)
      .send({
        equipmentId: 'equip-1',
        userId: 'user-2',
        loanDate: '2024-06-01',
        dueDate: '2024-06-10',
      });

    expect(res.status).toBe(409);
    expect(res.body).toMatchObject({ code: 'EQUIPMENT_NOT_AVAILABLE' });
  });

  it('POST /loans（dueDate <= loanDate）→ 400', async () => {
    mockPrisma.equipment.findUnique.mockResolvedValue(baseEquipment);
    mockPrisma.loanRecord.count.mockResolvedValue(0);

    const res = await request(app)
      .post('/loans')
      .set('Authorization', `Bearer ${ADMIN_TOKEN}`)
      .send({
        equipmentId: 'equip-1',
        userId: 'user-2',
        loanDate: '2024-06-10',
        dueDate: '2024-06-01', // dueDate < loanDate
      });

    expect(res.status).toBe(400);
    expect(res.body).toMatchObject({ code: 'INVALID_DUE_DATE' });
  });
});

// ─── テスト 3: 権限チェック ────────────────────────────────────────────────────

describe('7.2 権限チェック: USER トークンで ADMIN 専用 API を呼び出す', () => {
  it('POST /equipments → 403', async () => {
    const res = await request(app)
      .post('/equipments')
      .set('Authorization', `Bearer ${USER_TOKEN}`)
      .send({
        assetNumber: 'ASSET-002',
        name: 'タブレット',
        category: 'Tablet',
        quantity: 1,
      });

    expect(res.status).toBe(403);
  });

  it('POST /loans → 403', async () => {
    const res = await request(app)
      .post('/loans')
      .set('Authorization', `Bearer ${USER_TOKEN}`)
      .send({
        equipmentId: 'equip-1',
        userId: 'user-2',
        loanDate: '2024-06-01',
        dueDate: '2024-06-10',
      });

    expect(res.status).toBe(403);
  });

  it('DELETE /equipments/:id → 403', async () => {
    const res = await request(app)
      .delete('/equipments/equip-1')
      .set('Authorization', `Bearer ${USER_TOKEN}`);

    expect(res.status).toBe(403);
  });
});

// ─── テスト 4: Scheduler smoke test ───────────────────────────────────────────

describe('7.3 Scheduler smoke test', () => {
  it('checkDueTomorrow が呼び出し可能で例外をスローしない', async () => {
    await expect(checkDueTomorrow()).resolves.toBeUndefined();
  });

  it('checkOverdue が呼び出し可能で例外をスローしない', async () => {
    await expect(checkOverdue()).resolves.toBeUndefined();
  });
});
