/**
 * アカウントAPI
 * アカウントの一覧取得・作成・削除のAPIリクエストを提供する
 */
import apiClient from './client'

const accountApi = {
  /** アカウント一覧を取得する */
  getAll() {
    return apiClient.get('/api/accounts/')
  },

  /** アカウントを新規作成する */
  create(data) {
    return apiClient.post('/api/accounts/', data)
  },

  /** アカウントを削除する */
  delete(id) {
    return apiClient.delete(`/api/accounts/${id}`)
  },
}

export default accountApi
