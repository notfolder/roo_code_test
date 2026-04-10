import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import apiClient from '@/api/client'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || '')
  const user = ref(null)

  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.role === 'admin')

  function decodeToken(t) {
    try {
      const payload = JSON.parse(atob(t.split('.')[1]))
      return payload
    } catch {
      return null
    }
  }

  function restoreFromStorage() {
    const saved = localStorage.getItem('token')
    if (saved) {
      token.value = saved
      const payload = decodeToken(saved)
      if (payload) {
        user.value = { id: parseInt(payload.sub), role: payload.role }
      }
    }
  }

  async function login(login_id, password) {
    const res = await apiClient.post('auth/login', { login_id, password })
    token.value = res.data.access_token
    localStorage.setItem('token', token.value)
    const payload = decodeToken(token.value)
    if (payload) {
      user.value = { id: parseInt(payload.sub), role: payload.role }
    }
  }

  function logout() {
    token.value = ''
    user.value = null
    localStorage.removeItem('token')
    window.location.href = '/login'
  }

  return { token, user, isAuthenticated, isAdmin, login, logout, restoreFromStorage }
})
