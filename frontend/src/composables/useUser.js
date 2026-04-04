// ユーザーAPI呼び出しと状態管理
import { ref } from 'vue'
import apiClient from '../api/client.js'

export function useUser() {
  const users = ref([])
  const loading = ref(false)
  const error = ref('')

  async function fetchUsers() {
    loading.value = true
    error.value = ''
    try {
      const res = await apiClient.get('/api/users')
      users.value = res.data
    } catch (e) {
      error.value = e.response?.data?.detail || '取得に失敗しました'
    } finally {
      loading.value = false
    }
  }

  async function createUser(loginId, username, password, role) {
    const res = await apiClient.post('/api/users', { login_id: loginId, username, password, role })
    return res.data
  }

  async function updateUser(id, username, role) {
    const res = await apiClient.put(`/api/users/${id}`, { username, role })
    return res.data
  }

  async function deleteUser(id) {
    await apiClient.delete(`/api/users/${id}`)
  }

  return { users, loading, error, fetchUsers, createUser, updateUser, deleteUser }
}
