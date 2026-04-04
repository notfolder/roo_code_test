import cron from 'node-cron';
import { prisma } from './lib/prisma';
import {
  sendReturnReminder,
  sendOverdueNotification,
  LoanRecordWithRelations,
} from './services/notificationService';

export async function checkDueTomorrow(): Promise<void> {
  const tomorrow = new Date();
  tomorrow.setDate(tomorrow.getDate() + 1);
  tomorrow.setHours(0, 0, 0, 0);

  const dayAfterTomorrow = new Date(tomorrow);
  dayAfterTomorrow.setDate(dayAfterTomorrow.getDate() + 1);

  const records = await prisma.loanRecord.findMany({
    where: {
      dueDate: {
        gte: tomorrow,
        lt: dayAfterTomorrow,
      },
      returnedAt: null,
    },
    include: {
      equipment: true,
      user: true,
    },
  });

  for (const record of records) {
    await sendReturnReminder(record.userId, record as LoanRecordWithRelations);
  }

  console.log(`[Scheduler] checkDueTomorrow: ${records.length} reminder(s) sent.`);
}

export async function checkOverdue(): Promise<void> {
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  const records = await prisma.loanRecord.findMany({
    where: {
      dueDate: {
        lt: today,
      },
      returnedAt: null,
    },
    include: {
      equipment: true,
      user: true,
    },
  });

  for (const record of records) {
    await sendOverdueNotification(record.userId, record as LoanRecordWithRelations);
  }

  console.log(`[Scheduler] checkOverdue: ${records.length} overdue notification(s) sent.`);
}

export function startScheduler(): void {
  cron.schedule('0 9 * * *', async () => {
    console.log('[Scheduler] Running daily checks at 9:00 AM...');
    await checkDueTomorrow();
    await checkOverdue();
  });

  console.log('[Scheduler] Scheduler started. Daily checks scheduled at 9:00 AM.');
}
