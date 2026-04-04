import bcrypt from 'bcryptjs';
import { prisma } from '../lib/prisma';
import type { UserRole } from '../types';

const SALT_ROUNDS = 10;

export async function findUserByEmail(email: string) {
  return prisma.user.findUnique({ where: { email } });
}

export async function findUserById(id: string) {
  return prisma.user.findUnique({ where: { id } });
}

export async function createUser(data: {
  name: string;
  email: string;
  password: string;
  role?: UserRole;
}) {
  const hashedPassword = await bcrypt.hash(data.password, SALT_ROUNDS);
  return prisma.user.create({
    data: {
      name: data.name,
      email: data.email,
      password: hashedPassword,
      role: data.role ?? 'USER',
    },
  });
}

export async function validatePassword(
  plainPassword: string,
  hashedPassword: string,
): Promise<boolean> {
  return bcrypt.compare(plainPassword, hashedPassword);
}
