// ログイン状態・ロール・トークン管理（共通処理）
import { ref, computed } from 'vue'
import apiClient from '../api/client.js'

const accessToken = ref(localStorage.getItem('access_token') || '')
const userRole = ref(localStorage.getItem('user_role') || '')
const username = ref(localStorage.getItem('username') || '')

export function useAuth() {
  const isLoggedIn = computed(() => !!accessToken.value)
  const isAdmin = computed(() => userRole.value === 'admin')

  async function login(loginId, password) {
    const res = await apiClient.post('/api/auth/login', { login_id: loginId, password })
    accessToken.value = res.data.access_token
    userRole.value = res.data.role
    username.value = res.data.username
    localStorage.setItem('access_token', res.data.access_token)
    localStorage.setItem('user_role', res.data.role)
    localStorage.setItem('username', res.data.username)
  }

  function logout() {
    accessToken.value = ''
    userRole.value = ''
    username.value = ''
    localStorage.removeItem('access_token')
    localStorage.removeItem('user_role')
    localStorage.removeItem('username')
  }

  return { isLoggedIn, isAdmin, username, login, logout }
}
