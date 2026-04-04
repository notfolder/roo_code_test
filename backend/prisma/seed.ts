import { PrismaClient } from '@prisma/client';
import bcrypt from 'bcryptjs';

const prisma = new PrismaClient();

async function main() {
  const adminPassword = await bcrypt.hash('admin1234', 10);
  const userPassword = await bcrypt.hash('user1234', 10);

  const admin = await prisma.user.upsert({
    where: { email: 'admin@example.com' },
    update: {},
    create: {
      name: '管理者',
      email: 'admin@example.com',
      password: adminPassword,
      role: 'ADMIN',
    },
  });

  const user = await prisma.user.upsert({
    where: { email: 'user@example.com' },
    update: {},
    create: {
      name: '一般ユーザー',
      email: 'user@example.com',
      password: userPassword,
      role: 'USER',
    },
  });

  console.log('Seeded users:');
  console.log(`  ADMIN: ${admin.email} / admin1234`);
  console.log(`  USER:  ${user.email} / user1234`);
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(() => prisma.$disconnect());
