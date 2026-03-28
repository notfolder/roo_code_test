/**
 * 認証API
 * ログイン・ログアウトのAPIリクエストを提供する
 */
import apiClient from './client'

const authApi = {
  /** ログイン：アカウント名とパスワードでJWTトークンを取得する */
  login(accountName, password) {
    return apiClient.post('/api/auth/login', {
      account_name: accountName,
      password,
    })
  },

  /** ログアウト */
  logout() {
    return apiClient.post('/api/auth/logout')
  },
}

export default authApi
