// Axiosインスタンス・Authorizationヘッダー付与・401インターセプト（共通処理）
import axios from 'axios'

const apiClient = axios.create({
  baseURL: '/',
})

// リクエストインターセプター：localStorageからJWTトークンを取得してヘッダーに付与する
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// レスポンスインターセプター：401の場合はログイン画面へリダイレクトする
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token')
      localStorage.removeItem('user_role')
      localStorage.removeItem('username')
      window.location.href = '/'
    }
    return Promise.reject(error)
  }
)

export default apiClient
