import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';
import { JwtPayload, UserRole } from '../types';

const JWT_SECRET = process.env.JWT_SECRET || 'changeme';

/**
 * JWT 検証ミドルウェア
 * Authorization: Bearer <token> からトークンを取得・検証し、
 * 成功時は req.user に JwtPayload をセットする。
 */
export const authenticate = (req: Request, res: Response, next: NextFunction): void => {
  const authHeader = req.headers.authorization;

  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    res.status(401).json({ message: 'トークンが提供されていません' });
    return;
  }

  const token = authHeader.slice(7); // "Bearer " の後ろ

  try {
    const payload = jwt.verify(token, JWT_SECRET) as JwtPayload;
    req.user = payload;
    next();
  } catch {
    res.status(401).json({ message: 'トークンが無効または期限切れです' });
  }
};

/**
 * ロールガードファクトリ
 * authenticate の後に使用する。
 * req.user.role が指定ロールに含まれない場合は 403 を返す。
 *
 * 例: router.get('/admin', authenticate, requireRole('ADMIN'), handler)
 */
export const requireRole = (...roles: UserRole[]) => {
  return (req: Request, res: Response, next: NextFunction): void => {
    if (!req.user || !roles.includes(req.user.role)) {
      res.status(403).json({ message: 'アクセス権限がありません' });
      return;
    }
    next();
  };
};
