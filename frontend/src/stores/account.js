/**
 * アカウントストア
 * アカウント一覧データの取得・管理を行う
 */
import { defineStore } from 'pinia'
import { ref } from 'vue'
import accountApi from '../api/account'

export const useAccountStore = defineStore('account', () => {
  // アカウント一覧データ
  const items = ref([])
  // ローディング状態
  const loading = ref(false)

  /** アカウント一覧を取得する */
  async function fetchAll() {
    loading.value = true
    try {
      const response = await accountApi.getAll()
      items.value = response.data
    } finally {
      loading.value = false
    }
  }

  /** アカウントを新規作成する */
  async function create(data) {
    const response = await accountApi.create(data)
    items.value.push(response.data)
    return response.data
  }

  /** アカウントを削除する */
  async function remove(id) {
    await accountApi.delete(id)
    items.value = items.value.filter((a) => a.id !== id)
  }

  return { items, loading, fetchAll, create, remove }
})
