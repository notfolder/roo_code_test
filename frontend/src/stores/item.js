import { defineStore } from 'pinia'
import { ref } from 'vue'
import apiClient from '@/api/client'

export const useItemStore = defineStore('item', () => {
  const items = ref([])

  async function fetchItems() {
    const res = await apiClient.get('items')
    items.value = res.data
  }

  async function createItem(data) {
    const res = await apiClient.post('items', data)
    return res.data
  }

  async function updateItem(id, data) {
    const res = await apiClient.put(`items/${id}`, data)
    return res.data
  }

  async function deleteItem(id) {
    await apiClient.delete(`items/${id}`)
  }

  return { items, fetchItems, createItem, updateItem, deleteItem }
})
