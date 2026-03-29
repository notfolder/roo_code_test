import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import client from '../api/client.js'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('access_token') || null)
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))

  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.role === 'admin')

  async function login(loginId, password) {
    const res = await client.post('/auth/login', { login_id: loginId, password })
    token.value = res.data.access_token
    user.value = {
      id: res.data.user_id,
      name: res.data.name,
      role: res.data.role,
    }
    localStorage.setItem('access_token', token.value)
    localStorage.setItem('user', JSON.stringify(user.value))
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('user')
  }

  return { token, user, isAuthenticated, isAdmin, login, logout }
})
