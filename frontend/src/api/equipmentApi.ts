import { apiClient } from './client'
import type { Equipment, PaginatedResponse } from '../types'

export const getEquipments = (
  page: number = 1,
  size: number = 20,
): Promise<PaginatedResponse<Equipment>> =>
  apiClient.get('/equipments', { params: { page, size } }).then((r) => r.data)

export const searchEquipments = (params: {
  q?: string
  category?: string
  status?: string
  page?: number
  size?: number
}): Promise<PaginatedResponse<Equipment>> =>
  apiClient.get('/equipments/search', { params }).then((r) => r.data)

export const createEquipment = (data: {
  assetNumber: string
  name: string
  category: string
  quantity: number
}): Promise<Equipment> =>
  apiClient.post('/equipments', data).then((r) => r.data)

export const updateEquipment = (
  id: string,
  data: { name?: string; category?: string; quantity?: number },
): Promise<Equipment> =>
  apiClient.put(`/equipments/${id}`, data).then((r) => r.data)

export const disposeEquipment = (id: string): Promise<Equipment> =>
  apiClient.delete(`/equipments/${id}`).then((r) => r.data)
