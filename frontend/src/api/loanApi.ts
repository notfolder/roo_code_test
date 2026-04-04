import { apiClient } from './client'
import type { LoanRecord } from '../types'

export const createLoan = (data: {
  equipmentId: string
  userId: string
  loanDate: string
  dueDate: string
}): Promise<LoanRecord> =>
  apiClient.post('/loans', data).then((r) => r.data)

export const returnLoan = (loanId: string): Promise<LoanRecord> =>
  apiClient.post(`/loans/${loanId}/return`).then((r) => r.data)

export const getLoansByUser = (userId: string): Promise<LoanRecord[]> =>
  apiClient.get(`/loans/user/${userId}`).then((r) => r.data)

export const getLoansByEquipment = (equipmentId: string): Promise<LoanRecord[]> =>
  apiClient.get(`/loans/equipment/${equipmentId}`).then((r) => r.data)
