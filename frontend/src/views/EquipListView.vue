<template>
  <v-container class="pa-4">
    <v-row class="mb-2" align="center" justify="space-between">
      <v-col cols="12" md="4">
        <v-text-field v-model="keyword" label="名称/分類" density="comfortable" clearable @keyup.enter="fetchEquipments" />
      </v-col>
      <v-col cols="12" md="3">
        <v-select v-model="status" :items="statusItems" label="状態" density="comfortable" clearable />
      </v-col>
      <v-col cols="12" md="2">
        <v-btn color="primary" block @click="fetchEquipments" :loading="loading">検索</v-btn>
      </v-col>
    </v-row>

    <v-data-table :headers="headers" :items="equipments" :loading="loading" item-key="id">
      <template #item.actions="{ item }">
        <v-btn size="small" color="primary" @click="goReserve(item)">予約へ</v-btn>
      </template>
    </v-data-table>
  </v-container>
</template>

<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const api = axios.create({ baseURL: import.meta.env.VITE_API_BASE || 'http://localhost:8000' })
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

const loading = ref(false)
const equipments = ref([])
const keyword = ref('')
const status = ref(null)
const statusItems = ['available', 'reserved', 'loaned', 'overdue', 'retired']

const headers = [
  { title: '名称', key: 'name' },
  { title: '分類', key: 'category' },
  { title: '状態', key: 'status' },
  { title: '資産番号', key: 'asset_tag' },
  { title: '型番', key: 'model' },
  { title: '操作', key: 'actions', sortable: false },
]

const fetchEquipments = async () => {
  loading.value = true
  try {
    const res = await api.get('/equipments', {
      params: {
        name: keyword.value || undefined,
        status: status.value || undefined,
      },
    })
    equipments.value = res.data
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const goReserve = (item) => {
  router.push({ path: '/reservations', query: { equipment_id: item.id } })
}

onMounted(fetchEquipments)
</script>
