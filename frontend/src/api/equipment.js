/**
 * 備品API
 * 備品の一覧取得・登録・編集・削除のAPIリクエストを提供する
 */
import apiClient from './client'

const equipmentApi = {
  /** 備品一覧を取得する（availableOnly=trueで貸出可能な備品のみ） */
  getAll(availableOnly = false) {
    return apiClient.get('/api/equipment/', {
      params: { available_only: availableOnly },
    })
  },

  /** 備品を新規登録する */
  create(data) {
    return apiClient.post('/api/equipment/', data)
  },

  /** 備品情報を更新する */
  update(id, data) {
    return apiClient.put(`/api/equipment/${id}`, data)
  },

  /** 備品を削除する */
  delete(id) {
    return apiClient.delete(`/api/equipment/${id}`)
  },
}

export default equipmentApi
