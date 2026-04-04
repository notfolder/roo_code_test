import { checkDueTomorrow, checkOverdue } from '../scheduler';

jest.mock('../lib/prisma', () => ({
  prisma: {
    loanRecord: {
      findMany: jest.fn(),
    },
  },
}));

jest.mock('../services/notificationService', () => ({
  sendReturnReminder: jest.fn(),
  sendOverdueNotification: jest.fn(),
}));

import { prisma } from '../lib/prisma';
import { sendReturnReminder, sendOverdueNotification } from '../services/notificationService';

const mockFindMany = prisma.loanRecord.findMany as jest.MockedFunction<
  typeof prisma.loanRecord.findMany
>;
const mockSendReturnReminder = sendReturnReminder as jest.MockedFunction<typeof sendReturnReminder>;
const mockSendOverdueNotification = sendOverdueNotification as jest.MockedFunction<
  typeof sendOverdueNotification
>;

const baseUser = {
  id: 'user-1',
  name: 'テストユーザー',
  email: 'test@example.com',
  role: 'USER' as const,
  createdAt: new Date(),
  updatedAt: new Date(),
};

const baseEquipment = {
  id: 'equip-1',
  assetNumber: 'ASSET-001',
  name: 'ノートPC',
  category: 'PC',
  quantity: 1,
  status: 'ON_LOAN' as const,
  createdAt: new Date(),
  updatedAt: new Date(),
};

const tomorrow = new Date();
tomorrow.setDate(tomorrow.getDate() + 1);
tomorrow.setHours(0, 0, 0, 0);

const yesterday = new Date();
yesterday.setDate(yesterday.getDate() - 1);
yesterday.setHours(0, 0, 0, 0);

const baseLoanDueTomorrow = {
  id: 'loan-1',
  equipmentId: 'equip-1',
  userId: 'user-1',
  loanDate: new Date(),
  dueDate: tomorrow,
  returnedAt: null,
  createdAt: new Date(),
  updatedAt: new Date(),
  equipment: baseEquipment,
  user: baseUser,
};

const baseLoanOverdue = {
  id: 'loan-2',
  equipmentId: 'equip-1',
  userId: 'user-1',
  loanDate: new Date(),
  dueDate: yesterday,
  returnedAt: null,
  createdAt: new Date(),
  updatedAt: new Date(),
  equipment: baseEquipment,
  user: baseUser,
};

beforeEach(() => {
  jest.clearAllMocks();
});

// ─── checkDueTomorrow ──────────────────────────────────────────────────────────

describe('checkDueTomorrow', () => {
  it('翌日が返却予定日の未返却レコードがある場合 → sendReturnReminder が呼ばれる', async () => {
    mockFindMany.mockResolvedValue([baseLoanDueTomorrow] as any);

    await checkDueTomorrow();

    expect(mockSendReturnReminder).toHaveBeenCalledTimes(1);
    expect(mockSendReturnReminder).toHaveBeenCalledWith(
      baseLoanDueTomorrow.userId,
      baseLoanDueTomorrow,
    );
  });

  it('該当レコードがない場合 → sendReturnReminder が呼ばれない', async () => {
    mockFindMany.mockResolvedValue([]);

    await checkDueTomorrow();

    expect(mockSendReturnReminder).not.toHaveBeenCalled();
  });
});

// ─── checkOverdue ──────────────────────────────────────────────────────────────

describe('checkOverdue', () => {
  it('返却期限超過の未返却レコードがある場合 → sendOverdueNotification が呼ばれる', async () => {
    mockFindMany.mockResolvedValue([baseLoanOverdue] as any);

    await checkOverdue();

    expect(mockSendOverdueNotification).toHaveBeenCalledTimes(1);
    expect(mockSendOverdueNotification).toHaveBeenCalledWith(
      baseLoanOverdue.userId,
      baseLoanOverdue,
    );
  });

  it('該当レコードがない場合 → sendOverdueNotification が呼ばれない', async () => {
    mockFindMany.mockResolvedValue([]);

    await checkOverdue();

    expect(mockSendOverdueNotification).not.toHaveBeenCalled();
  });
});
