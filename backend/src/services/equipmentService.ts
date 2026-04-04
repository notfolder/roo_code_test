import prisma from '../lib/prisma';

export async function createEquipment(data: {
  assetNumber: string;
  name: string;
  category: string;
  quantity: number;
}) {
  const existing = await prisma.equipment.findUnique({
    where: { assetNumber: data.assetNumber },
  });
  if (existing) {
    throw { code: 'DUPLICATE_ASSET_NUMBER' };
  }
  return prisma.equipment.create({ data });
}

export async function getEquipments(page: number, size: number) {
  const [items, total] = await Promise.all([
    prisma.equipment.findMany({
      skip: (page - 1) * size,
      take: size,
      orderBy: { createdAt: 'desc' },
    }),
    prisma.equipment.count(),
  ]);
  return { items, total, page, size };
}

export async function getEquipmentById(id: string) {
  return prisma.equipment.findUnique({ where: { id } });
}

export async function updateEquipment(
  id: string,
  data: { name?: string; category?: string; quantity?: number },
) {
  return prisma.equipment.update({ where: { id }, data });
}

export async function disposeEquipment(id: string) {
  const equipment = await prisma.equipment.findUnique({ where: { id } });
  if (!equipment) return null;
  if (equipment.status === 'ON_LOAN') {
    throw { code: 'EQUIPMENT_ON_LOAN' };
  }
  return prisma.equipment.update({
    where: { id },
    data: { status: 'DISPOSED' },
  });
}
