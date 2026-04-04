import { Request, Response } from 'express';
import * as equipmentService from '../services/equipmentService';

export async function createEquipment(req: Request, res: Response): Promise<void> {
  const { assetNumber, name, category, quantity } = req.body;
  if (!assetNumber || !name || !category || quantity == null) {
    res.status(400).json({ message: 'assetNumber, name, category, quantity は必須です' });
    return;
  }
  try {
    const equipment = await equipmentService.createEquipment({ assetNumber, name, category, quantity });
    res.status(201).json(equipment);
  } catch (err: any) {
    if (err?.code === 'DUPLICATE_ASSET_NUMBER') {
      res.status(409).json({ message: '管理番号が既に存在します', code: err.code });
      return;
    }
    throw err;
  }
}

export async function getEquipments(req: Request, res: Response): Promise<void> {
  const page = Math.max(1, parseInt(req.query.page as string) || 1);
  const size = Math.max(1, parseInt(req.query.size as string) || 20);
  const result = await equipmentService.getEquipments(page, size);
  res.json(result);
}

export async function getEquipmentById(req: Request, res: Response): Promise<void> {
  const equipment = await equipmentService.getEquipmentById(req.params.id);
  if (!equipment) {
    res.status(404).json({ message: '備品が見つかりません' });
    return;
  }
  res.json(equipment);
}

export async function updateEquipment(req: Request, res: Response): Promise<void> {
  const { name, category, quantity } = req.body;
  try {
    const equipment = await equipmentService.updateEquipment(req.params.id, { name, category, quantity });
    res.json(equipment);
  } catch (err: any) {
    if (err?.code === 'P2025') {
      res.status(404).json({ message: '備品が見つかりません' });
      return;
    }
    throw err;
  }
}

export async function disposeEquipment(req: Request, res: Response): Promise<void> {
  try {
    const equipment = await equipmentService.disposeEquipment(req.params.id);
    if (!equipment) {
      res.status(404).json({ message: '備品が見つかりません' });
      return;
    }
    res.json(equipment);
  } catch (err: any) {
    if (err?.code === 'EQUIPMENT_ON_LOAN') {
      res.status(409).json({ message: '貸出中の備品は廃棄できません', code: err.code });
      return;
    }
    throw err;
  }
}
