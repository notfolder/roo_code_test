import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';
import { authenticate, requireRole } from '../../middleware/auth';
import { JwtPayload } from '../../types';

const JWT_SECRET = 'changeme';

// モック用ヘルパー
function mockRes() {
  const res = {
    status: jest.fn().mockReturnThis(),
    json: jest.fn().mockReturnThis(),
  } as unknown as Response;
  return res;
}

function mockReq(overrides: Partial<Request> = {}): Request {
  return { headers: {}, ...overrides } as unknown as Request;
}

describe('authenticate middleware', () => {
  const next: NextFunction = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
    process.env.JWT_SECRET = JWT_SECRET;
  });

  it('Authorization ヘッダーなし → 401', () => {
    const req = mockReq();
    const res = mockRes();

    authenticate(req, res, next);

    expect(res.status).toHaveBeenCalledWith(401);
    expect(res.json).toHaveBeenCalledWith({ message: 'トークンが提供されていません' });
    expect(next).not.toHaveBeenCalled();
  });

  it('Bearer プレフィックスなし → 401', () => {
    const req = mockReq({ headers: { authorization: 'Token abc123' } });
    const res = mockRes();

    authenticate(req, res, next);

    expect(res.status).toHaveBeenCalledWith(401);
    expect(next).not.toHaveBeenCalled();
  });

  it('無効なトークン → 401', () => {
    const req = mockReq({ headers: { authorization: 'Bearer invalidtoken' } });
    const res = mockRes();

    authenticate(req, res, next);

    expect(res.status).toHaveBeenCalledWith(401);
    expect(res.json).toHaveBeenCalledWith({ message: 'トークンが無効または期限切れです' });
    expect(next).not.toHaveBeenCalled();
  });

  it('有効なトークン → req.user がセットされ next() が呼ばれる', () => {
    const payload: JwtPayload = { userId: 'user-1', email: 'test@example.com', role: 'USER' };
    const token = jwt.sign(payload, JWT_SECRET);
    const req = mockReq({ headers: { authorization: `Bearer ${token}` } });
    const res = mockRes();

    authenticate(req, res, next);

    expect(next).toHaveBeenCalled();
    expect(req.user).toMatchObject(payload);
    expect(res.status).not.toHaveBeenCalled();
  });
});

describe('requireRole middleware', () => {
  const next: NextFunction = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('req.user が ADMIN で requireRole("ADMIN") → next() が呼ばれる', () => {
    const req = mockReq({
      user: { userId: 'user-1', email: 'admin@example.com', role: 'ADMIN' },
    });
    const res = mockRes();

    requireRole('ADMIN')(req, res, next);

    expect(next).toHaveBeenCalled();
    expect(res.status).not.toHaveBeenCalled();
  });

  it('req.user が USER で requireRole("ADMIN") → 403', () => {
    const req = mockReq({
      user: { userId: 'user-2', email: 'user@example.com', role: 'USER' },
    });
    const res = mockRes();

    requireRole('ADMIN')(req, res, next);

    expect(res.status).toHaveBeenCalledWith(403);
    expect(res.json).toHaveBeenCalledWith({ message: 'アクセス権限がありません' });
    expect(next).not.toHaveBeenCalled();
  });

  it('req.user が未設定 → 403', () => {
    const req = mockReq();
    const res = mockRes();

    requireRole('ADMIN')(req, res, next);

    expect(res.status).toHaveBeenCalledWith(403);
    expect(next).not.toHaveBeenCalled();
  });
});
