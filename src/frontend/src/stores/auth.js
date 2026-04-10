import { defineStore } from 'pinia'

const TOKEN_KEY = 'equipment-token'
const ROLE_KEY = 'equipment-role'
const USER_ID_KEY = 'equipment-user-id'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem(TOKEN_KEY) || '',
    role: localStorage.getItem(ROLE_KEY) || '',
    userId: localStorage.getItem(USER_ID_KEY) || ''
  }),
  getters: {
    isAuthenticated: (state) => Boolean(state.token),
    isAdmin: (state) => state.role === 'admin'
  },
  actions: {
    setSession({ access_token, role, user_id }) {
      this.token = access_token
      this.role = role
      this.userId = user_id
      localStorage.setItem(TOKEN_KEY, access_token)
      localStorage.setItem(ROLE_KEY, role)
      localStorage.setItem(USER_ID_KEY, user_id)
    },
    clearSession() {
      this.token = ''
      this.role = ''
      this.userId = ''
      localStorage.removeItem(TOKEN_KEY)
      localStorage.removeItem(ROLE_KEY)
      localStorage.removeItem(USER_ID_KEY)
    }
  }
})
