// 備品API呼び出しと状態管理
import { ref } from 'vue'
import apiClient from '../api/client.js'

export function useEquipment() {
  const equipments = ref([])
  const loading = ref(false)
  const error = ref('')

  async function fetchEquipments() {
    loading.value = true
    error.value = ''
    try {
      const res = await apiClient.get('/api/equipments')
      equipments.value = res.data
    } catch (e) {
      error.value = e.response?.data?.detail || '取得に失敗しました'
    } finally {
      loading.value = false
    }
  }

  async function createEquipment(code, name) {
    const res = await apiClient.post('/api/equipments', { code, name })
    return res.data
  }

  async function updateEquipment(id, name) {
    const res = await apiClient.put(`/api/equipments/${id}`, { name })
    return res.data
  }

  async function deleteEquipment(id) {
    await apiClient.delete(`/api/equipments/${id}`)
  }

  async function lendEquipment(id, borrowerName) {
    const res = await apiClient.post(`/api/equipments/${id}/lend`, { borrower_name: borrowerName })
    return res.data
  }

  async function returnEquipment(id) {
    const res = await apiClient.post(`/api/equipments/${id}/return`)
    return res.data
  }

  return { equipments, loading, error, fetchEquipments, createEquipment, updateEquipment, deleteEquipment, lendEquipment, returnEquipment }
}
