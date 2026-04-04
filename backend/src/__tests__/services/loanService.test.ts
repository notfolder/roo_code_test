import * as loanService from '../../services/loanService';

jest.mock('../../lib/prisma', () => ({
  __esModule: true,
  default: {
    equipment: {
      findUnique: jest.fn(),
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
}));

jest.mock('../../services/notificationService', () => ({
  sendReturnCompleted: jest.fn(),
}));

import prisma from '../../lib/prisma';
import { sendReturnCompleted } from '../../services/notificationService';

const mockPrisma = prisma as jest.Mocked<typeof prisma> & {
  equipment: {
    findUnique: jest.MockedFunction<typeof prisma.equipment.findUnique>;
    update: jest.MockedFunction<typeof prisma.equipment.update>;
  };
  loanRecord: {
    findUnique: jest.MockedFunction<typeof prisma.loanRecord.findUnique>;
    findMany: jest.MockedFunction<typeof prisma.loanRecord.findMany>;
    count: jest.MockedFunction<typeof prisma.loanRecord.count>;
    create: jest.MockedFunction<typeof prisma.loanRecord.create>;
    update: jest.MockedFunction<typeof prisma.loanRecord.update>;
  };
  $transaction: jest.MockedFunction<typeof prisma.$transaction>;
};

const mockSendReturnCompleted = sendReturnCompleted as jest.MockedFunction<typeof sendReturnCompleted>;

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

const loanDate = new Date('2024-06-01');
const dueDate = new Date('2024-06-10');

const baseLoan = {
  id: 'loan-1',
  equipmentId: 'equip-1',
  userId: 'user-1',
  loanDate,
  dueDate,
  returnedAt: null,
  createdAt: new Date('2024-06-01'),
  updatedAt: new Date('2024-06-01'),
};

const baseLoanWithRelations = {
  ...baseLoan,
  equipment: baseEquipment,
  user: { id: 'user-1', name: 'テストユーザー', email: 'test@example.com', role: 'USER' as const, createdAt: new Date(), updatedAt: new Date() },
};

beforeEach(() => {
  jest.clearAllMocks();
});

// ─── createLoan ────────────────────────────────────────────────────────────────

describe('createLoan', () => {
  const input = { equipmentId: 'equip-1', userId: 'user-1', loanDate, dueDate };

  it('備品が存在しない → EQUIPMENT_NOT_FOUND エラー', async () => {
    mockPrisma.equipment.findUnique.mockResolvedValue(null);

    await expect(loanService.createLoan(input)).rejects.toMatchObject({
      code: 'EQUIPMENT_NOT_FOUND',
    });

    expect(mockPrisma.$transaction).not.toHaveBeenCalled();
  });

  it('備品が ON_LOAN → EQUIPMENT_NOT_AVAILABLE エラー', async () => {
    mockPrisma.equipment.findUnique.mockResolvedValue({ ...baseEquipment, status: 'ON_LOAN' as const });

    await expect(loanService.createLoan(input)).rejects.toMatchObject({
      code: 'EQUIPMENT_NOT_AVAILABLE',
    });

    expect(mockPrisma.$transaction).not.toHaveBeenCalled();
  });

  it('dueDate <= loanDate → INVALID_DUE_DATE エラー', async () => {
    mockPrisma.equipment.findUnique.mockResolvedValue(baseEquipment);

    await expect(
      loanService.createLoan({ ...input, dueDate: loanDate }),
    ).rejects.toMatchObject({ code: 'INVALID_DUE_DATE' });

    expect(mockPrisma.$transaction).not.toHaveBeenCalled();
  });

  it('未返却貸出が5件 → LOAN_LIMIT_EXCEEDED エラー', async () => {
    mockPrisma.equipment.findUnique.mockResolvedValue(baseEquipment);
    mockPrisma.loanRecord.count.mockResolvedValue(5);

    await expect(loanService.createLoan(input)).rejects.toMatchObject({
      code: 'LOAN_LIMIT_EXCEEDED',
    });

    expect(mockPrisma.$transaction).not.toHaveBeenCalled();
  });

  it('正常貸出 → LoanRecord を返す', async () => {
    mockPrisma.equipment.findUnique.mockResolvedValue(baseEquipment);
    mockPrisma.loanRecord.count.mockResolvedValue(0);
    mockPrisma.$transaction.mockImplementation(async (fn: any) => {
      const tx = {
        loanRecord: { create: jest.fn().mockResolvedValue(baseLoan) },
        equipment: { update: jest.fn().mockResolvedValue({ ...baseEquipment, status: 'ON_LOAN' }) },
      };
      return fn(tx);
    });

    const result = await loanService.createLoan(input);

    expect(result).toEqual(baseLoan);
    expect(mockPrisma.$transaction).toHaveBeenCalled();
  });
});

// ─── returnLoan ────────────────────────────────────────────────────────────────

describe('returnLoan', () => {
  it('LoanRecord が存在しない → LOAN_NOT_FOUND エラー', async () => {
    mockPrisma.loanRecord.findUnique.mockResolvedValue(null);

    await expect(loanService.returnLoan('loan-1')).rejects.toMatchObject({
      code: 'LOAN_NOT_FOUND',
    });

    expect(mockPrisma.$transaction).not.toHaveBeenCalled();
  });

  it('既に返却済み（returnedAt が設定済み）→ ALREADY_RETURNED エラー', async () => {
    mockPrisma.loanRecord.findUnique.mockResolvedValue({
      ...baseLoanWithRelations,
      returnedAt: new Date('2024-06-05'),
    } as any);

    await expect(loanService.returnLoan('loan-1')).rejects.toMatchObject({
      code: 'ALREADY_RETURNED',
    });

    expect(mockPrisma.$transaction).not.toHaveBeenCalled();
  });

  it('正常返却 → 返却済み LoanRecord を返す', async () => {
    const returnedAt = new Date('2024-06-05');
    const returnedLoan = { ...baseLoanWithRelations, returnedAt };

    mockPrisma.loanRecord.findUnique.mockResolvedValue(baseLoanWithRelations as any);
    mockPrisma.$transaction.mockImplementation(async (fn: any) => {
      const tx = {
        loanRecord: { update: jest.fn().mockResolvedValue(returnedLoan) },
        equipment: { update: jest.fn().mockResolvedValue({ ...baseEquipment, status: 'AVAILABLE' }) },
      };
      return fn(tx);
    });
    mockSendReturnCompleted.mockResolvedValue(undefined);

    const result = await loanService.returnLoan('loan-1');

    expect(result).toEqual(returnedLoan);
    expect(mockSendReturnCompleted).toHaveBeenCalledWith(returnedLoan.userId, returnedLoan);
  });
});

// ─── getLoansByUser ────────────────────────────────────────────────────────────

describe('getLoansByUser', () => {
  it('userId に紐づく LoanRecord を返す', async () => {
    const loans = [baseLoanWithRelations];
    mockPrisma.loanRecord.findMany.mockResolvedValue(loans as any);

    const result = await loanService.getLoansByUser('user-1');

    expect(result).toEqual(loans);
    expect(mockPrisma.loanRecord.findMany).toHaveBeenCalledWith({
      where: { userId: 'user-1' },
      orderBy: { returnedAt: 'desc' },
      include: {
        equipment: { select: { name: true } },
        user: { select: { name: true } },
      },
    });
  });
});

// ─── getLoansByEquipment ───────────────────────────────────────────────────────

describe('getLoansByEquipment', () => {
  it('equipmentId に紐づく LoanRecord を返す', async () => {
    const loans = [baseLoanWithRelations];
    mockPrisma.loanRecord.findMany.mockResolvedValue(loans as any);

    const result = await loanService.getLoansByEquipment('equip-1');

    expect(result).toEqual(loans);
    expect(mockPrisma.loanRecord.findMany).toHaveBeenCalledWith({
      where: { equipmentId: 'equip-1' },
      orderBy: { returnedAt: 'desc' },
      include: {
        equipment: { select: { name: true } },
        user: { select: { name: true } },
      },
    });
  });
});
