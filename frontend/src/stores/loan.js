/**
 * 貸出ストア
 * 貸出記録一覧データの取得・管理を行う
 */
import { defineStore } from 'pinia'
import { ref } from 'vue'
import loanApi from '../api/loan'

export const useLoanStore = defineStore('loan', () => {
  // 貸出記録一覧データ
  const items = ref([])
  // ローディング状態
  const loading = ref(false)

  /** 貸出記録一覧を取得する */
  async function fetchAll() {
    loading.value = true
    try {
      const response = await loanApi.getAll()
      items.value = response.data
    } finally {
      loading.value = false
    }
  }

  /** 貸出を登録する */
  async function create(equipmentId, borrowerAccountId) {
    const response = await loanApi.create(equipmentId, borrowerAccountId)
    items.value.unshift(response.data)
    return response.data
  }

  /** 返却を登録する */
  async function returnLoan(loanId) {
    const response = await loanApi.returnLoan(loanId)
    const index = items.value.findIndex((l) => l.id === loanId)
    if (index !== -1) items.value[index] = response.data
    return response.data
  }

  return { items, loading, fetchAll, create, returnLoan }
})
