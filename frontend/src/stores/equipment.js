import { defineStore } from 'pinia'
import { ref } from 'vue'
import client from '../api/client.js'

export const useEquipmentStore = defineStore('equipment', () => {
  const items = ref([])
  const loading = ref(false)
  const error = ref(null)

  async function fetchAll() {
    loading.value = true
    error.value = null
    try {
      const res = await client.get('/equipment/')
      items.value = res.data
    } catch (e) {
      error.value = e.response?.data?.detail || 'エラーが発生しました'
    } finally {
      loading.value = false
    }
  }

  async function create(data) {
    const res = await client.post('/equipment/', data)
    items.value.push(res.data)
    return res.data
  }

  async function update(id, data) {
    const res = await client.put(`/equipment/${id}`, data)
    const idx = items.value.findIndex((e) => e.id === id)
    if (idx !== -1) items.value[idx] = res.data
    return res.data
  }

  async function remove(id) {
    await client.delete(`/equipment/${id}`)
    items.value = items.value.filter((e) => e.id !== id)
  }

  return { items, loading, error, fetchAll, create, update, remove }
})
