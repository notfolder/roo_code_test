import { defineStore } from 'pinia'
import { ref } from 'vue'
import apiClient from '@/api/client'

export const useUserStore = defineStore('user', () => {
  const users = ref([])

  async function fetchUsers() {
    const res = await apiClient.get('users')
    users.value = res.data
  }

  async function createUser(data) {
    const res = await apiClient.post('users', data)
    return res.data
  }

  async function deleteUser(id) {
    await apiClient.delete(`users/${id}`)
  }

  return { users, fetchUsers, createUser, deleteUser }
})
