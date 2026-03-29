import { defineStore } from 'pinia'
import { ref } from 'vue'
import client from '../api/client.js'

export const useUserStore = defineStore('user', () => {
  const users = ref([])
  const loading = ref(false)
  const error = ref(null)

  async function fetchAll() {
    loading.value = true
    error.value = null
    try {
      const res = await client.get('/users/')
      users.value = res.data
    } catch (e) {
      error.value = e.response?.data?.detail || 'エラーが発生しました'
    } finally {
      loading.value = false
    }
  }

  async function create(data) {
    const res = await client.post('/users/', data)
    users.value.push(res.data)
    return res.data
  }

  async function update(id, data) {
    const res = await client.put(`/users/${id}`, data)
    const idx = users.value.findIndex((u) => u.id === id)
    if (idx !== -1) users.value[idx] = res.data
    return res.data
  }

  async function remove(id) {
    await client.delete(`/users/${id}`)
    users.value = users.value.filter((u) => u.id !== id)
  }

  return { users, loading, error, fetchAll, create, update, remove }
})
