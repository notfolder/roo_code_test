/**
 * 備品ストア
 * 備品一覧データの取得・管理を行う
 */
import { defineStore } from 'pinia'
import { ref } from 'vue'
import equipmentApi from '../api/equipment'

export const useEquipmentStore = defineStore('equipment', () => {
  // 備品一覧データ
  const items = ref([])
  // ローディング状態
  const loading = ref(false)

  /** 備品一覧を取得する（availableOnly=trueで貸出可能な備品のみ） */
  async function fetchAll(availableOnly = false) {
    loading.value = true
    try {
      const response = await equipmentApi.getAll(availableOnly)
      items.value = response.data
    } finally {
      loading.value = false
    }
  }

  /** 備品を新規登録する */
  async function create(data) {
    const response = await equipmentApi.create(data)
    items.value.push(response.data)
    return response.data
  }

  /** 備品情報を更新する */
  async function update(id, data) {
    const response = await equipmentApi.update(id, data)
    const index = items.value.findIndex((e) => e.id === id)
    if (index !== -1) items.value[index] = response.data
    return response.data
  }

  /** 備品を削除する */
  async function remove(id) {
    await equipmentApi.delete(id)
    items.value = items.value.filter((e) => e.id !== id)
  }

  return { items, loading, fetchAll, create, update, remove }
})
