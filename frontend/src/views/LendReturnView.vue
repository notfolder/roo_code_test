<template>
  <v-container class="pa-4" max-width="720">
    <v-card class="mb-4">
      <v-card-title>貸出登録（管理者）</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="createLending">
          <v-text-field v-model="reservationId" label="予約ID" required density="comfortable" />
          <v-text-field v-model="lendDate" label="貸出日 (YYYY-MM-DD)" required density="comfortable" />
          <v-alert v-if="lendMsg" :type="lendMsgType" dense class="my-2">{{ lendMsg }}</v-alert>
          <v-btn color="primary" type="submit" :loading="loadingLend">貸出登録</v-btn>
        </v-form>
      </v-card-text>
    </v-card>

    <v-card class="mb-4">
      <v-card-title>返却登録（管理者）</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="createReturn">
          <v-text-field v-model="lendingId" label="貸出ID" required density="comfortable" />
          <v-text-field v-model="returnDate" label="返却日 (YYYY-MM-DD)" required density="comfortable" />
          <v-text-field v-model="conditionNote" label="状態メモ" density="comfortable" />
          <v-alert v-if="returnMsg" :type="returnMsgType" dense class="my-2">{{ returnMsg }}</v-alert>
          <v-btn color="success" type="submit" :loading="loadingReturn">返却登録</v-btn>
        </v-form>
      </v-card-text>
    </v-card>

    <v-card>
      <v-card-title>貸出一覧</v-card-title>
      <v-card-text>
        <v-data-table :headers="lendHeaders" :items="lendingList" :loading="listLoading" item-key="id" />
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'

const api = axios.create({ baseURL: import.meta.env.VITE_API_BASE || 'http://localhost:8000' })
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

const reservationId = ref('')
const lendDate = ref('')
const lendingId = ref('')
const returnDate = ref('')
const conditionNote = ref('')
const lendMsg = ref('')
const lendMsgType = ref('success')
const returnMsg = ref('')
const returnMsgType = ref('success')
const loadingLend = ref(false)
const loadingReturn = ref(false)
const listLoading = ref(false)
const lendingList = ref([])

const lendHeaders = [
  { title: 'ID', key: 'id' },
  { title: '予約ID', key: 'reservation_id' },
  { title: '貸出日', key: 'lend_date' },
  { title: '期限日', key: 'due_date' },
  { title: '状態', key: 'status' },
]

const fetchLendings = async () => {
  listLoading.value = true
  try {
    const res = await api.get('/lendings')
    lendingList.value = res.data
  } catch (e) {
    console.error(e)
  } finally {
    listLoading.value = false
  }
}

const createLending = async () => {
  lendMsg.value = ''
  lendMsgType.value = 'success'
  loadingLend.value = true
  try {
    await api.post('/lendings', { reservation_id: reservationId.value, lend_date: lendDate.value })
    lendMsg.value = '貸出を登録しました'
    await fetchLendings()
  } catch (e) {
    lendMsgType.value = 'error'
    lendMsg.value = e.response?.data?.detail || 'エラーが発生しました'
  } finally {
    loadingLend.value = false
  }
}

const createReturn = async () => {
  returnMsg.value = ''
  returnMsgType.value = 'success'
  loadingReturn.value = true
  try {
    await api.post('/returns', {
      lending_id: lendingId.value,
      return_date: returnDate.value,
      condition_note: conditionNote.value || undefined,
    })
    returnMsg.value = '返却を登録しました'
    await fetchLendings()
  } catch (e) {
    returnMsgType.value = 'error'
    returnMsg.value = e.response?.data?.detail || 'エラーが発生しました'
  } finally {
    loadingReturn.value = false
  }
}

onMounted(fetchLendings)
</script>
