<template>
  <v-app>
    <v-main>
      <v-container>
        <div class="d-flex justify-space-between align-center mb-4">
          <div class="text-h6">予約一覧 / 作成</div>
          <v-btn color="primary" @click="fetchReservations">再読込</v-btn>
        </div>
        <v-card class="mb-4" outlined>
          <v-card-title>予約作成</v-card-title>
          <v-card-text>
            <v-form @submit.prevent="create">
              <v-text-field v-model="itemId" label="備品ID" required></v-text-field>
              <v-text-field v-model="start" label="開始日(YYYY-MM-DD)" required></v-text-field>
              <v-text-field v-model="end" label="返却予定日(YYYY-MM-DD)" required></v-text-field>
              <v-btn type="submit" color="primary" class="mt-2">予約する</v-btn>
              <div class="error" v-if="error">{{ error }}</div>
            </v-form>
          </v-card-text>
        </v-card>
        <v-simple-table>
          <thead>
            <tr>
              <th>備品ID</th>
              <th>開始</th>
              <th>終了</th>
              <th>状態</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="r in reservations" :key="r.id">
              <td>{{ r.item_id }}</td>
              <td>{{ r.start_date }}</td>
              <td>{{ r.end_date }}</td>
              <td>{{ r.status }}</td>
              <td>
                <v-btn size="small" color="error" @click="cancel(r.id)" v-if="r.status==='reserved'">キャンセル</v-btn>
              </td>
            </tr>
          </tbody>
        </v-simple-table>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'

const reservations = ref([])
const itemId = ref('')
const start = ref('')
const end = ref('')
const error = ref('')

const fetchReservations = async () => {
  const res = await api.get('/reservations')
  reservations.value = res.data
}

const create = async () => {
  error.value = ''
  try {
    await api.post('/reservations', { item_id: itemId.value, start_date: start.value, end_date: end.value })
    await fetchReservations()
  } catch (e) {
    error.value = '予約に失敗しました（重複や日付を確認してください）'
  }
}

const cancel = async (id) => {
  try {
    await api.post(`/reservations/${id}/cancel`)
    await fetchReservations()
  } catch (e) {
    error.value = 'キャンセルに失敗しました'
  }
}

onMounted(fetchReservations)
</script>

<style scoped>
.error { color: red; }
</style>
