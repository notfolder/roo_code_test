import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const apiClient = axios.create({
  baseURL: '/api/',
})

apiClient.interceptors.request.use((config) => {
  const authStore = useAuthStore()
  if (authStore.token) {
    config.headers['Authorization'] = `Bearer ${authStore.token}`
  }
  return config
})

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      const url = error.config?.url || ''
      if (!url.includes('auth/login')) {
        const authStore = useAuthStore()
        authStore.logout()
      }
    }
    return Promise.reject(error)
  }
)

export default apiClient
