import * as searchService from '../../services/searchService';

jest.mock('../../lib/prisma', () => ({
  __esModule: true,
  default: {
    equipment: {
      findMany: jest.fn(),
      count: jest.fn(),
    },
  },
}));

import prisma from '../../lib/prisma';

const mockPrisma = prisma as jest.Mocked<typeof prisma> & {
  equipment: {
    findMany: jest.MockedFunction<typeof prisma.equipment.findMany>;
    count: jest.MockedFunction<typeof prisma.equipment.count>;
  };
};

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

beforeEach(() => {
  jest.clearAllMocks();
  mockPrisma.equipment.findMany.mockResolvedValue([baseEquipment]);
  mockPrisma.equipment.count.mockResolvedValue(1);
});

// ─── キーワード検索 ────────────────────────────────────────────────────────────

describe('キーワード検索（q パラメータ）', () => {
  it('q が指定された場合、OR 条件（name/category/assetNumber の contains）が Prisma に渡される', async () => {
    await searchService.searchEquipments({ q: 'PC', page: 1, size: 10 });

    expect(mockPrisma.equipment.findMany).toHaveBeenCalledWith(
      expect.objectContaining({
        where: expect.objectContaining({
          OR: [
            { name: { contains: 'PC', mode: 'insensitive' } },
            { category: { contains: 'PC', mode: 'insensitive' } },
            { assetNumber: { contains: 'PC', mode: 'insensitive' } },
          ],
        }),
      }),
    );
  });
});

// ─── カテゴリフィルタ ──────────────────────────────────────────────────────────

describe('カテゴリフィルタ', () => {
  it('category が指定された場合、where.category が設定される', async () => {
    await searchService.searchEquipments({ category: 'PC', page: 1, size: 10 });

    expect(mockPrisma.equipment.findMany).toHaveBeenCalledWith(
      expect.objectContaining({
        where: expect.objectContaining({ category: 'PC' }),
      }),
    );
  });
});

// ─── ステータスフィルタ ────────────────────────────────────────────────────────

describe('ステータスフィルタ', () => {
  it('status が指定された場合、where.status が設定される', async () => {
    await searchService.searchEquipments({ status: 'AVAILABLE', page: 1, size: 10 });

    expect(mockPrisma.equipment.findMany).toHaveBeenCalledWith(
      expect.objectContaining({
        where: expect.objectContaining({ status: 'AVAILABLE' }),
      }),
    );
  });
});

// ─── ページネーション ──────────────────────────────────────────────────────────

describe('ページネーション', () => {
  it('page=2, size=10 の場合、skip=10, take=10 で呼ばれる', async () => {
    await searchService.searchEquipments({ page: 2, size: 10 });

    expect(mockPrisma.equipment.findMany).toHaveBeenCalledWith(
      expect.objectContaining({ skip: 10, take: 10 }),
    );
  });
});

// ─── 検索結果ゼロ件 ────────────────────────────────────────────────────────────

describe('検索結果ゼロ件', () => {
  it('items が空の場合、message: "該当する備品が見つかりません" が含まれる', async () => {
    mockPrisma.equipment.findMany.mockResolvedValue([]);
    mockPrisma.equipment.count.mockResolvedValue(0);

    const result = await searchService.searchEquipments({ page: 1, size: 10 });

    expect(result.items).toHaveLength(0);
    expect(result.message).toBe('該当する備品が見つかりません');
  });
});

// ─── 検索結果あり ──────────────────────────────────────────────────────────────

describe('検索結果あり', () => {
  it('items がある場合、message は含まれない', async () => {
    const result = await searchService.searchEquipments({ page: 1, size: 10 });

    expect(result.items).toHaveLength(1);
    expect(result.message).toBeUndefined();
  });
});
