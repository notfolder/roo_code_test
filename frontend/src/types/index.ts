export interface User {
  id: string
  name: string
  email: string
  role: 'USER' | 'ADMIN'
}

export enum EquipmentStatus {
  AVAILABLE = '利用可能',
  ON_LOAN = '貸出中',
  DISPOSED = '廃棄済み',
}

export interface Equipment {
  id: string
  assetNumber: string
  name: string
  category: string
  quantity: number
  status: EquipmentStatus
  createdAt: string
  updatedAt: string
}

export interface LoanRecord {
  id: string
  equipmentId: string
  userId: string
  loanDate: string
  dueDate: string
  returnedAt: string | null
  createdAt: string
}

export interface PaginatedResponse<T> {
  data: T[]
  total: number
  page: number
  size: number
}
