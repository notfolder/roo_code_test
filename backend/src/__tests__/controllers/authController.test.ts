import { Request, Response } from 'express';
import { login } from '../../controllers/authController';

// userService をモック化
jest.mock('../../services/userService', () => ({
  findUserByEmail: jest.fn(),
  validatePassword: jest.fn(),
}));

import { findUserByEmail, validatePassword } from '../../services/userService';

const mockFindUserByEmail = findUserByEmail as jest.MockedFunction<typeof findUserByEmail>;
const mockValidatePassword = validatePassword as jest.MockedFunction<typeof validatePassword>;

function mockRes() {
  const res = {
    status: jest.fn().mockReturnThis(),
    json: jest.fn().mockReturnThis(),
  } as unknown as Response;
  return res;
}

function mockReq(body: Record<string, unknown> = {}): Request {
  return { body } as unknown as Request;
}

const dummyUser = {
  id: 'user-1',
  name: 'テストユーザー',
  email: 'test@example.com',
  password: '$2a$10$hashedpassword',
  role: 'USER' as const,
  createdAt: new Date(),
  updatedAt: new Date(),
};

describe('login controller', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    process.env.JWT_SECRET = 'test-secret';
  });

  it('email なし → 400', async () => {
    const req = mockReq({ password: 'pass123' });
    const res = mockRes();

    await login(req, res);

    expect(res.status).toHaveBeenCalledWith(400);
    expect(res.json).toHaveBeenCalledWith({ message: 'email と password は必須です' });
  });

  it('password なし → 400', async () => {
    const req = mockReq({ email: 'test@example.com' });
    const res = mockRes();

    await login(req, res);

    expect(res.status).toHaveBeenCalledWith(400);
    expect(res.json).toHaveBeenCalledWith({ message: 'email と password は必須です' });
  });

  it('email・password 両方なし → 400', async () => {
    const req = mockReq({});
    const res = mockRes();

    await login(req, res);

    expect(res.status).toHaveBeenCalledWith(400);
  });

  it('存在しないメール → 401', async () => {
    mockFindUserByEmail.mockResolvedValue(null);
    const req = mockReq({ email: 'notfound@example.com', password: 'pass123' });
    const res = mockRes();

    await login(req, res);

    expect(res.status).toHaveBeenCalledWith(401);
    expect(res.json).toHaveBeenCalledWith({
      message: 'メールアドレスまたはパスワードが正しくありません',
    });
  });

  it('パスワード不一致 → 401', async () => {
    mockFindUserByEmail.mockResolvedValue(dummyUser);
    mockValidatePassword.mockResolvedValue(false);
    const req = mockReq({ email: 'test@example.com', password: 'wrongpass' });
    const res = mockRes();

    await login(req, res);

    expect(res.status).toHaveBeenCalledWith(401);
    expect(res.json).toHaveBeenCalledWith({
      message: 'メールアドレスまたはパスワードが正しくありません',
    });
  });

  it('正常ログイン → 200 + token', async () => {
    mockFindUserByEmail.mockResolvedValue(dummyUser);
    mockValidatePassword.mockResolvedValue(true);
    const req = mockReq({ email: 'test@example.com', password: 'correctpass' });
    const res = mockRes();

    await login(req, res);

    expect(res.status).not.toHaveBeenCalled(); // デフォルト 200
    expect(res.json).toHaveBeenCalledWith(
      expect.objectContaining({
        token: expect.any(String),
        user: {
          id: dummyUser.id,
          name: dummyUser.name,
          email: dummyUser.email,
          role: dummyUser.role,
        },
      }),
    );
  });
});
