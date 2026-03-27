<template>
  <v-container class="pa-4" max-width="720">
    <v-card class="mb-4">
      <v-card-title>予約作成</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="create">
          <v-text-field v-model="equipmentId" label="備品ID" required density="comfortable" />
          <v-text-field v-model="startDate" label="開始日 (YYYY-MM-DD)" required density="comfortable" />
          <v-text-field v-model="endDate" label="終了日 (YYYY-MM-DD)" required density="comfortable" />
          <v-alert v-if="message" :type="messageType" dense class="my-2">{{ message }}</v-alert>
          <v-btn color="primary" type="submit" :loading="loading">予約作成</v-btn>
        </v-form>
      </v-card-text>
    </v-card>

    <v-card>
      <v-card-title>自分の予約一覧</v-card-title>
      <v-card-text>
        <v-data-table :headers="headers" :items="reservations" :loading="loading" item-key="id">
          <template #item.actions="{ item }">
            <v-btn size="small" color="error" @click="cancel(item.id)" :disabled="item.status !== 'confirmed'">キャンセル</v-btn>
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const api = axios.create({ baseURL: import.meta.env.VITE_API_BASE || 'http://localhost:8000' })
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

const equipmentId = ref(route.query.equipment_id || '')
const startDate = ref('')
const endDate = ref('')
const reservations = ref([])
const loading = ref(false)
const message = ref('')
const messageType = ref('success')

const headers = [
  { title: '備品ID', key: 'equipment_id' },
  { title: '開始日', key: 'start_date' },
  { title: '終了日', key: 'end_date' },
  { title: '状態', key: 'status' },
  { title: '操作', key: 'actions', sortable: false },
]

const fetchReservations = async () => {
  loading.value = true
  try {
    const res = await api.get('/reservations')
    reservations.value = res.data
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const create = async () => {
  message.value = ''
  messageType.value = 'success'
  loading.value = true
  try {
    await api.post('/reservations', {
      equipment_id: equipmentId.value,
      start_date: startDate.value,
      end_date: endDate.value,
    })
    message.value = '予約を作成しました'
    await fetchReservations()
  } catch (e) {
    messageType.value = 'error'
    message.value = e.response?.data?.detail || 'エラーが発生しました'
  } finally {
    loading.value = false
  }
}

const cancel = async (id) => {
  loading.value = true
  try {
    await api.delete(`/reservations/${id}`)
    await fetchReservations()
  } catch (e) {
    messageType.value = 'error'
    message.value = e.response?.data?.detail || 'キャンセルに失敗しました'
  } finally {
    loading.value = false
  }
}

onMounted(fetchReservations)
</script>
