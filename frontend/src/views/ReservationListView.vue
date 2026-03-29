<template>
  <AppLayout>
    <div class="d-flex justify-space-between align-center mb-4">
      <h1 class="text-h5">予約一覧</h1>
      <v-btn color="primary" to="/reservations/create">+ 予約を登録する</v-btn>
    </div>
    <v-card>
      <v-data-table
        :headers="headers"
        :items="reservationStore.reservations"
        :loading="reservationStore.loading"
        no-data-text="予約はありません"
      >
        <template #item.status="{ item }">
          <v-chip :color="statusColor(item.status)" size="small">
            {{ statusLabel(item.status) }}
          </v-chip>
        </template>
        <template #item.actions="{ item }">
          <v-btn
            v-if="item.status === 'pending'"
            size="small"
            color="error"
            variant="text"
            :loading="cancelingId === item.id"
            @click="handleCancel(item.id)"
          >
            取消
          </v-btn>
          <span v-else>—</span>
        </template>
      </v-data-table>
    </v-card>
    <v-snackbar v-model="snackbar" :color="snackbarColor" timeout="3000">
      {{ snackbarMsg }}
    </v-snackbar>
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import AppLayout from './AppLayout.vue'
import { useReservationStore } from '../stores/reservation.js'
import { useAuthStore } from '../stores/auth.js'

const reservationStore = useReservationStore()
const authStore = useAuthStore()

const cancelingId = ref(null)
const snackbar = ref(false)
const snackbarMsg = ref('')
const snackbarColor = ref('success')

const headers = computed(() => {
  const base = [
    { title: '備品名', key: 'equipment_name' },
    { title: '貸出開始日', key: 'planned_start_date' },
    { title: '返却予定日', key: 'planned_return_date' },
    { title: '状態', key: 'status' },
    { title: '操作', key: 'actions', sortable: false },
  ]
  if (authStore.isAdmin) {
    base.splice(1, 0, { title: '予約者', key: 'user_name' })
  }
  return base
})

function statusLabel(s) {
  if (s === 'pending') return '予約中'
  if (s === 'cancelled') return 'キャンセル済'
  if (s === 'loaned') return '貸出済'
  return s
}

function statusColor(s) {
  if (s === 'pending') return 'warning'
  if (s === 'cancelled') return 'default'
  if (s === 'loaned') return 'success'
  return 'default'
}

async function handleCancel(id) {
  cancelingId.value = id
  try {
    await reservationStore.cancelReservation(id)
    snackbarMsg.value = '予約をキャンセルしました'
    snackbarColor.value = 'success'
  } catch (e) {
    snackbarMsg.value = e.response?.data?.detail || 'キャンセルに失敗しました'
    snackbarColor.value = 'error'
  } finally {
    cancelingId.value = null
    snackbar.value = true
  }
}

onMounted(async () => {
  await reservationStore.fetchReservations()
})
</script>
