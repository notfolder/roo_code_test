import * as equipmentService from '../../services/equipmentService';

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
  },
}));

import prisma from '../../lib/prisma';

const mockPrisma = prisma as jest.Mocked<typeof prisma> & {
  equipment: {
    findUnique: jest.MockedFunction<typeof prisma.equipment.findUnique>;
    findMany: jest.MockedFunction<typeof prisma.equipment.findMany>;
    count: jest.MockedFunction<typeof prisma.equipment.count>;
    create: jest.MockedFunction<typeof prisma.equipment.create>;
    update: jest.MockedFunction<typeof prisma.equipment.update>;
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
});

// ─── createEquipment ───────────────────────────────────────────────────────────

describe('createEquipment', () => {
  it('正常登録 → 備品オブジェクトを返す', async () => {
    mockPrisma.equipment.findUnique.mockResolvedValue(null);
    mockPrisma.equipment.create.mockResolvedValue(baseEquipment);

    const result = await equipmentService.createEquipment({
      assetNumber: 'ASSET-001',
      name: 'ノートPC',
      category: 'PC',
      quantity: 1,
    });

    expect(result).toEqual(baseEquipment);
    expect(mockPrisma.equipment.create).toHaveBeenCalledWith({
      data: { assetNumber: 'ASSET-001', name: 'ノートPC', category: 'PC', quantity: 1 },
    });
  });

  it('重複 assetNumber → DUPLICATE_ASSET_NUMBER エラーをスロー', async () => {
    mockPrisma.equipment.findUnique.mockResolvedValue(baseEquipment);

    await expect(
      equipmentService.createEquipment({
        assetNumber: 'ASSET-001',
        name: 'ノートPC',
        category: 'PC',
        quantity: 1,
      }),
    ).rejects.toMatchObject({ code: 'DUPLICATE_ASSET_NUMBER' });

    expect(mockPrisma.equipment.create).not.toHaveBeenCalled();
  });
});

// ─── getEquipments ─────────────────────────────────────────────────────────────

describe('getEquipments', () => {
  it('ページネーション付きで items と total を返す', async () => {
    const items = [baseEquipment];
    mockPrisma.equipment.findMany.mockResolvedValue(items);
    mockPrisma.equipment.count.mockResolvedValue(5);

    const result = await equipmentService.getEquipments(2, 10);

    expect(result).toEqual({ items, total: 5, page: 2, size: 10 });
    expect(mockPrisma.equipment.findMany).toHaveBeenCalledWith({
      skip: 10,
      take: 10,
      orderBy: { createdAt: 'desc' },
    });
  });
});

// ─── getEquipmentById ──────────────────────────────────────────────────────────

describe('getEquipmentById', () => {
  it('存在する ID → 備品を返す', async () => {
    mockPrisma.equipment.findUnique.mockResolvedValue(baseEquipment);

    const result = await equipmentService.getEquipmentById('equip-1');

    expect(result).toEqual(baseEquipment);
    expect(mockPrisma.equipment.findUnique).toHaveBeenCalledWith({ where: { id: 'equip-1' } });
  });

  it('存在しない ID → null を返す', async () => {
    mockPrisma.equipment.findUnique.mockResolvedValue(null);

    const result = await equipmentService.getEquipmentById('nonexistent');

    expect(result).toBeNull();
  });
});

// ─── updateEquipment ───────────────────────────────────────────────────────────

describe('updateEquipment', () => {
  it('正常更新 → 更新後の備品を返す', async () => {
    const updated = { ...baseEquipment, name: '更新後PC', quantity: 2 };
    mockPrisma.equipment.update.mockResolvedValue(updated);

    const result = await equipmentService.updateEquipment('equip-1', {
      name: '更新後PC',
      quantity: 2,
    });

    expect(result).toEqual(updated);
    expect(mockPrisma.equipment.update).toHaveBeenCalledWith({
      where: { id: 'equip-1' },
      data: { name: '更新後PC', quantity: 2 },
    });
  });
});

// ─── disposeEquipment ──────────────────────────────────────────────────────────

describe('disposeEquipment', () => {
  it('AVAILABLE の備品 → DISPOSED に変更して返す', async () => {
    const disposed = { ...baseEquipment, status: 'DISPOSED' as const };
    mockPrisma.equipment.findUnique.mockResolvedValue(baseEquipment);
    mockPrisma.equipment.update.mockResolvedValue(disposed);

    const result = await equipmentService.disposeEquipment('equip-1');

    expect(result).toEqual(disposed);
    expect(mockPrisma.equipment.update).toHaveBeenCalledWith({
      where: { id: 'equip-1' },
      data: { status: 'DISPOSED' },
    });
  });

  it('ON_LOAN の備品 → EQUIPMENT_ON_LOAN エラーをスロー', async () => {
    mockPrisma.equipment.findUnique.mockResolvedValue({
      ...baseEquipment,
      status: 'ON_LOAN' as const,
    });

    await expect(equipmentService.disposeEquipment('equip-1')).rejects.toMatchObject({
      code: 'EQUIPMENT_ON_LOAN',
    });

    expect(mockPrisma.equipment.update).not.toHaveBeenCalled();
  });

  it('存在しない ID → null を返す', async () => {
    mockPrisma.equipment.findUnique.mockResolvedValue(null);

    const result = await equipmentService.disposeEquipment('nonexistent');

    expect(result).toBeNull();
    expect(mockPrisma.equipment.update).not.toHaveBeenCalled();
  });
});
