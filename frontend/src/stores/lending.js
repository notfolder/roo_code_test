import { defineStore } from 'pinia'
import { ref } from 'vue'
import apiClient from '@/api/client'

export const useLendingStore = defineStore('lending', () => {
  const lendingRecords = ref([])

  async function fetchLendingRecords() {
    const res = await apiClient.get('lending_records')
    lendingRecords.value = res.data
  }

  async function createLendingRecord(data) {
    const res = await apiClient.post('lending_records', data)
    return res.data
  }

  async function returnItem(id, data) {
    const res = await apiClient.put(`lending_records/${id}/return`, data)
    return res.data
  }

  return { lendingRecords, fetchLendingRecords, createLendingRecord, returnItem }
})
