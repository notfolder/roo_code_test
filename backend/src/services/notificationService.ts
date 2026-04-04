import { LoanRecord, Equipment, User } from '@prisma/client';

export type LoanRecordWithRelations = LoanRecord & {
  equipment: Equipment;
  user: User;
};

export async function sendReturnReminder(
  userId: string,
  loanRecord: LoanRecordWithRelations,
): Promise<void> {
  console.log(
    `[Notification] Return reminder sent to userId=${userId}, loanId=${loanRecord.id}, equipment=${loanRecord.equipment.name}, dueDate=${loanRecord.dueDate}`,
  );
}

export async function sendOverdueNotification(
  userId: string,
  loanRecord: LoanRecordWithRelations,
): Promise<void> {
  console.log(
    `[Notification] Overdue notification sent to userId=${userId}, loanId=${loanRecord.id}, equipment=${loanRecord.equipment.name}, dueDate=${loanRecord.dueDate}`,
  );
}

export async function sendReturnCompleted(
  userId: string,
  loanRecord: LoanRecordWithRelations,
): Promise<void> {
  console.log(
    `[Notification] Return completed sent to userId=${userId}, loanId=${loanRecord.id}, equipment=${loanRecord.equipment.name}, returnedAt=${loanRecord.returnedAt}`,
  );
}
