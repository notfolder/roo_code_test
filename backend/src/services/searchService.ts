import prisma from '../lib/prisma';
import { EquipmentStatus } from '@prisma/client';

interface SearchParams {
  q?: string;
  category?: string;
  status?: string;
  page: number;
  size: number;
}

export async function searchEquipments(params: SearchParams) {
  const { q, category, status, page, size } = params;

  const where: Record<string, unknown> = {};

  if (q) {
    where.OR = [
      { name: { contains: q, mode: 'insensitive' } },
      { category: { contains: q, mode: 'insensitive' } },
      { assetNumber: { contains: q, mode: 'insensitive' } },
    ];
  }

  if (category) {
    where.category = category;
  }

  if (status) {
    where.status = status as EquipmentStatus;
  }

  const [items, total] = await Promise.all([
    prisma.equipment.findMany({
      where,
      skip: (page - 1) * size,
      take: size,
      orderBy: { createdAt: 'desc' },
    }),
    prisma.equipment.count({ where }),
  ]);

  const result: {
    items: typeof items;
    total: number;
    page: number;
    size: number;
    message?: string;
  } = { items, total, page, size };

  if (items.length === 0) {
    result.message = '該当する備品が見つかりません';
  }

  return result;
}
