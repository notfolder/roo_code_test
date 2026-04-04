import axios from 'axios'

const TOKEN_KEY = 'auth_token'

export const apiClient = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

// リクエストインターセプター: JWT トークンを Authorization ヘッダーに付与
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem(TOKEN_KEY)
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error),
)

// レスポンスインターセプター: 401 の場合はトークンを削除してログインへリダイレクト
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem(TOKEN_KEY)
      window.location.href = '/login'
    }
    return Promise.reject(error)
  },
)

export const setAuthToken = (token: string) => {
  localStorage.setItem(TOKEN_KEY, token)
}

export const clearAuthToken = () => {
  localStorage.removeItem(TOKEN_KEY)
}
