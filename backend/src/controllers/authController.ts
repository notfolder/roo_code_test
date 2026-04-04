import { Request, Response } from 'express';
import jwt from 'jsonwebtoken';
import { findUserByEmail, validatePassword } from '../services/userService';

export async function login(req: Request, res: Response): Promise<void> {
  const { email, password } = req.body;

  if (!email || !password) {
    res.status(400).json({ message: 'email と password は必須です' });
    return;
  }

  const user = await findUserByEmail(email);
  if (!user) {
    res.status(401).json({ message: 'メールアドレスまたはパスワードが正しくありません' });
    return;
  }

  const isValid = await validatePassword(password, user.password);
  if (!isValid) {
    res.status(401).json({ message: 'メールアドレスまたはパスワードが正しくありません' });
    return;
  }

  const secret = process.env.JWT_SECRET as string;
  const token = jwt.sign(
    { userId: user.id, email: user.email, role: user.role },
    secret,
    { expiresIn: '24h' },
  );

  res.json({
    token,
    user: {
      id: user.id,
      name: user.name,
      email: user.email,
      role: user.role,
    },
  });
}
