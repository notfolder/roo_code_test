import axios from 'axios'
import { useAuthStore } from '../stores/auth.js'

// axiosインスタンス: 全APIリクエストは /api/ 以下に送信する
const apiClient = axios.create({
  baseURL: '/api',
})

// リクエストインターセプター: JWTトークンをAuthorizationヘッダーに付与する
apiClient.interceptors.request.use((config) => {
  const authStore = useAuthStore()
  if (authStore.token) {
    config.headers.Authorization = `Bearer ${authStore.token}`
  }
  return config
})

// レスポンスインターセプター: 401エラー時はログアウト処理を行う
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      const authStore = useAuthStore()
      authStore.logout()
    }
    return Promise.reject(error)
  }
)

// 認証API
export const login = (loginId, password) =>
  apiClient.post('/auth/login', { login_id: loginId, password })

// 備品API
export const getEquipmentList = () => apiClient.get('/equipment')
export const createEquipment = (data) => apiClient.post('/equipment', data)
export const updateEquipment = (id, data) => apiClient.put(`/equipment/${id}`, data)
export const deleteEquipment = (id) => apiClient.delete(`/equipment/${id}`)

// 貸出・返却API
export const getLendingHistory = () => apiClient.get('/lending')
export const getActiveLending = () => apiClient.get('/lending/active')
export const createLending = (data) => apiClient.post('/lending', data)
export const returnLending = (id, returnedAt) =>
  apiClient.put(`/lending/${id}/return`, { returned_at: returnedAt })
