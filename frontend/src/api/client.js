/**
 * axiosインスタンスの共通設定
 * JWTトークンのAuthorizationヘッダー付与と、401エラー時のログアウト処理を一元管理する
 */
import axios from 'axios'

// axiosインスタンスを作成する（全APIモジュールで共用）
const apiClient = axios.create({
  baseURL: '/',
  headers: { 'Content-Type': 'application/json' },
})

// リクエストインターセプター：JWTトークンをAuthorizationヘッダーに付与する
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// レスポンスインターセプター：401エラー時はトークンを削除してログイン画面にリダイレクトする
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token')
      localStorage.removeItem('role')
      // ログイン画面以外にいる場合のみリダイレクトする
      if (window.location.pathname !== '/login') {
        window.location.href = '/login'
      }
    }
    return Promise.reject(error)
  }
)

export default apiClient
