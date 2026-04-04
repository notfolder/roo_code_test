import prisma from '../lib/prisma';
import { sendReturnCompleted } from './notificationService';

export async function createLoan(data: {
  equipmentId: string;
  userId: string;
  loanDate: Date;
  dueDate: Date;
}) {
  const equipment = await prisma.equipment.findUnique({ where: { id: data.equipmentId } });
  if (!equipment) {
    throw { code: 'EQUIPMENT_NOT_FOUND' };
  }
  if (equipment.status !== 'AVAILABLE') {
    throw { code: 'EQUIPMENT_NOT_AVAILABLE' };
  }
  if (data.dueDate <= data.loanDate) {
    throw { code: 'INVALID_DUE_DATE' };
  }

  const activeLoans = await prisma.loanRecord.count({
    where: { userId: data.userId, returnedAt: null },
  });
  if (activeLoans >= 5) {
    throw { code: 'LOAN_LIMIT_EXCEEDED' };
  }

  return prisma.$transaction(async (tx) => {
    const loan = await tx.loanRecord.create({ data });
    await tx.equipment.update({
      where: { id: data.equipmentId },
      data: { status: 'ON_LOAN' },
    });
    return loan;
  });
}

export async function returnLoan(loanId: string) {
  const loan = await prisma.loanRecord.findUnique({
    where: { id: loanId },
    include: { equipment: true, user: true },
  });
  if (!loan) {
    throw { code: 'LOAN_NOT_FOUND' };
  }
  if (loan.returnedAt !== null) {
    throw { code: 'ALREADY_RETURNED' };
  }

  const returnedAt = new Date();
  const updated = await prisma.$transaction(async (tx) => {
    const record = await tx.loanRecord.update({
      where: { id: loanId },
      data: { returnedAt },
      include: { equipment: true, user: true },
    });
    await tx.equipment.update({
      where: { id: loan.equipmentId },
      data: { status: 'AVAILABLE' },
    });
    return record;
  });

  await sendReturnCompleted(updated.userId, updated);
  return updated;
}

export async function getLoansByUser(userId: string) {
  return prisma.loanRecord.findMany({
    where: { userId },
    orderBy: { returnedAt: 'desc' },
    include: {
      equipment: { select: { name: true } },
      user: { select: { name: true } },
    },
  });
}

export async function getLoansByEquipment(equipmentId: string) {
  return prisma.loanRecord.findMany({
    where: { equipmentId },
    orderBy: { returnedAt: 'desc' },
    include: {
      equipment: { select: { name: true } },
      user: { select: { name: true } },
    },
  });
}
