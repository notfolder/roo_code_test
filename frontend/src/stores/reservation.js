import { defineStore } from 'pinia'
import { ref } from 'vue'
import client from '../api/client.js'

export const useReservationStore = defineStore('reservation', () => {
  const reservations = ref([])
  const pendingReservations = ref([])
  const loading = ref(false)
  const error = ref(null)

  async function fetchReservations() {
    loading.value = true
    error.value = null
    try {
      const res = await client.get('/reservations/')
      reservations.value = res.data
    } catch (e) {
      error.value = e.response?.data?.detail || 'エラーが発生しました'
    } finally {
      loading.value = false
    }
  }

  async function createReservation(data) {
    const res = await client.post('/reservations/', data)
    reservations.value.push(res.data)
    return res.data
  }

  async function cancelReservation(id) {
    const res = await client.put(`/reservations/${id}/cancel`)
    const idx = reservations.value.findIndex((r) => r.id === id)
    if (idx !== -1) reservations.value[idx] = res.data
    return res.data
  }

  async function fetchPendingByEquipment(equipmentId) {
    loading.value = true
    error.value = null
    try {
      const res = await client.get(`/reservations/pending/${equipmentId}`)
      pendingReservations.value = res.data
    } catch (e) {
      pendingReservations.value = []
      error.value = e.response?.data?.detail || 'エラーが発生しました'
    } finally {
      loading.value = false
    }
  }

  return {
    reservations,
    pendingReservations,
    loading,
    error,
    fetchReservations,
    createReservation,
    cancelReservation,
    fetchPendingByEquipment,
  }
})
