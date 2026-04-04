import { Request, Response } from 'express';
import * as searchService from '../services/searchService';

export async function searchEquipments(req: Request, res: Response): Promise<void> {
  const q = req.query.q as string | undefined;
  const category = req.query.category as string | undefined;
  const status = req.query.status as string | undefined;
  const page = Math.max(1, parseInt(req.query.page as string) || 1);
  const size = Math.max(1, parseInt(req.query.size as string) || 20);

  const result = await searchService.searchEquipments({ q, category, status, page, size });
  res.json(result);
}
