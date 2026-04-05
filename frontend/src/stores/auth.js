import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

// 認証状態管理ストア
export const useAuthStore = defineStore('auth', () => {
  // localStorageから初期値を読み込む
  const token = ref(localStorage.getItem('access_token') || null)

  const isLoggedIn = computed(() => token.value !== null)

  function setToken(newToken) {
    token.value = newToken
    localStorage.setItem('access_token', newToken)
  }

  function logout() {
    token.value = null
    localStorage.removeItem('access_token')
  }

  return { token, isLoggedIn, setToken, logout }
})
