import { defineStore } from 'pinia'
import { ref } from 'vue'
import client from '../api/client.js'

export const useLoanStore = defineStore('loan', () => {
  const loans = ref([])
  const activeLoans = ref([])
  const loading = ref(false)
  const error = ref(null)

  async function fetchAll() {
    loading.value = true
    error.value = null
    try {
      const res = await client.get('/loans/')
      loans.value = res.data
    } catch (e) {
      error.value = e.response?.data?.detail || 'エラーが発生しました'
    } finally {
      loading.value = false
    }
  }

  async function fetchActive() {
    loading.value = true
    error.value = null
    try {
      const res = await client.get('/loans/active')
      activeLoans.value = res.data
    } catch (e) {
      error.value = e.response?.data?.detail || 'エラーが発生しました'
    } finally {
      loading.value = false
    }
  }

  async function create(data) {
    const res = await client.post('/loans/', data)
    loans.value.push(res.data)
    return res.data
  }

  async function returnLoan(loanId, returnDate) {
    const res = await client.put(`/loans/${loanId}/return`, { return_date: returnDate })
    const idx = loans.value.findIndex((l) => l.id === loanId)
    if (idx !== -1) loans.value[idx] = res.data
    activeLoans.value = activeLoans.value.filter((l) => l.id !== loanId)
    return res.data
  }

  return { loans, activeLoans, loading, error, fetchAll, fetchActive, create, returnLoan }
})
