import { Request, Response } from 'express';
import * as loanService from '../services/loanService';

export async function createLoan(req: Request, res: Response): Promise<void> {
  const { equipmentId, userId, loanDate, dueDate } = req.body;
  if (!equipmentId || !userId || !loanDate || !dueDate) {
    res.status(400).json({ message: 'equipmentId, userId, loanDate, dueDate は必須です' });
    return;
  }
  try {
    const loan = await loanService.createLoan({
      equipmentId,
      userId,
      loanDate: new Date(loanDate),
      dueDate: new Date(dueDate),
    });
    res.status(201).json(loan);
  } catch (err: any) {
    if (err?.code === 'EQUIPMENT_NOT_FOUND') {
      res.status(404).json({ message: '備品が見つかりません', code: err.code });
    } else if (err?.code === 'EQUIPMENT_NOT_AVAILABLE') {
      res.status(409).json({ message: '備品は現在貸出できません', code: err.code });
    } else if (err?.code === 'INVALID_DUE_DATE') {
      res.status(400).json({ message: '返却期限は貸出日より後の日付を指定してください', code: err.code });
    } else if (err?.code === 'LOAN_LIMIT_EXCEEDED') {
      res.status(409).json({ message: '貸出上限（5件）に達しています', code: err.code });
    } else {
      throw err;
    }
  }
}

export async function returnLoan(req: Request, res: Response): Promise<void> {
  try {
    const loan = await loanService.returnLoan(req.params.id);
    res.json(loan);
  } catch (err: any) {
    if (err?.code === 'LOAN_NOT_FOUND') {
      res.status(404).json({ message: '貸出記録が見つかりません', code: err.code });
    } else if (err?.code === 'ALREADY_RETURNED') {
      res.status(409).json({ message: '既に返却済みです', code: err.code });
    } else {
      throw err;
    }
  }
}

export async function getLoansByUser(req: Request, res: Response): Promise<void> {
  const loans = await loanService.getLoansByUser(req.params.userId);
  res.json(loans);
}

export async function getLoansByEquipment(req: Request, res: Response): Promise<void> {
  const loans = await loanService.getLoansByEquipment(req.params.equipmentId);
  res.json(loans);
}
