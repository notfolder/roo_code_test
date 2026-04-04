// ユーザーロール
export type UserRole = 'USER' | 'ADMIN';

// 備品ステータス
export enum EquipmentStatus {
  AVAILABLE = '利用可能',
  ON_LOAN = '貸出中',
  DISPOSED = '廃棄済み',
}

// JWT ペイロード
export interface JwtPayload {
  userId: string;
  email: string;
  role: UserRole;
}

// Express Request 拡張
declare global {
  namespace Express {
    interface Request {
      user?: JwtPayload;
    }
  }
}
