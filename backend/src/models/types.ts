// ユーザー役割
export type UserRole = "admin" | "user";

// ユーザーエンティティ
export interface User {
  id: number;
  loginId: string;
  name: string;
  role: UserRole;
  passwordHash: string;
  passwordExpiresAt: Date;
  isLocked: boolean;
  createdAt: Date;
  updatedAt: Date;
  deletedAt: Date | null;
}

// 備品ステータス
export type EquipmentStatus = "available" | "broken" | "maintenance";

// 備品エンティティ
export interface Equipment {
  id: number;
  managementNumber: string;
  name: string;
  category: string;
  location: string;
  status: EquipmentStatus;
  description: string;
  createdAt: Date;
  updatedAt: Date;
  deletedAt: Date | null;
}

// 予約ステータス
export type ReservationStatus = "reserved" | "cancelled" | "completed";

// 予約エンティティ
export interface Reservation {
  id: number;
  equipmentId: number;
  userId: number;
  purpose: string;
  startAt: Date;
  endAt: Date;
  status: ReservationStatus;
  cancelledAt: Date | null;
  usageStartAt: Date | null;
  usageEndAt: Date | null;
  createdAt: Date;
  updatedAt: Date;
}

// 操作ログエンティティ
export interface OperationLog {
  id: number;
  actorUserId: number | null;
  action: string;
  targetType: string;
  targetId: number | null;
  detail: string;
  createdAt: Date;
}
