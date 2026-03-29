<template>
  <AppLayout>
    <h1 class="text-h5 mb-4">貸出登録</h1>
    <v-card class="pa-4" max-width="600">
      <v-form @submit.prevent="handleSubmit">
        <v-select
          v-model="form.equipment_id"
          :items="availableEquipment"
          item-title="name"
          item-value="id"
          label="備品"
          required
        />
        <div v-if="form.equipment_id" class="mb-3">
          <div class="text-subtitle-2 mb-1">選択した備品の予約一覧</div>
          <v-table density="compact" v-if="reservationStore.pendingReservations.length > 0">
            <thead>
              <tr>
                <th>予約者</th>
                <th>貸出開始予定日</th>
                <th>返却予定日</th>
                <th>状態</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="r in reservationStore.pendingReservations" :key="r.id">
                <td>{{ r.user_name }}</td>
                <td>{{ r.planned_start_date }}</td>
                <td>{{ r.planned_return_date }}</td>
                <td>予約中</td>
              </tr>
            </tbody>
          </v-table>
          <v-alert v-else density="compact" type="info" variant="tonal">この備品の予約はありません</v-alert>
        </div>
        <v-select
          v-model="form.borrower_user_id"
          :items="userStore.users"
          item-title="name"
          item-value="id"
          label="借用者"
          required
        />
        <v-text-field v-model="form.loan_date" label="貸出日" type="date" required />
        <v-alert v-if="errorMsg" type="error" class="mb-3">{{ errorMsg }}</v-alert>
        <v-alert v-if="successMsg" type="success" class="mb-3">{{ successMsg }}</v-alert>
        <div class="d-flex gap-2">
          <v-btn type="submit" color="primary" :loading="loading">登録</v-btn>
          <v-btn variant="text" to="/">キャンセル</v-btn>
        </div>
      </v-form>
    </v-card>
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import AppLayout from './AppLayout.vue'
import { useEquipmentStore } from '../stores/equipment.js'
import { useUserStore } from '../stores/user.js'
import { useLoanStore } from '../stores/loan.js'
import { useReservationStore } from '../stores/reservation.js'

const equipmentStore = useEquipmentStore()
const userStore = useUserStore()
const loanStore = useLoanStore()
const reservationStore = useReservationStore()

const loading = ref(false)
const errorMsg = ref('')
const successMsg = ref('')

const today = new Date().toISOString().split('T')[0]
const form = ref({ equipment_id: null, borrower_user_id: null, loan_date: today })

const availableEquipment = computed(() => equipmentStore.items.filter((e) => e.status === 'available'))

watch(
  () => form.value.equipment_id,
  async (newId) => {
    if (newId) {
      await reservationStore.fetchPendingByEquipment(newId)
    } else {
      reservationStore.pendingReservations = []
    }
  },
)

async function handleSubmit() {
  errorMsg.value = ''
  successMsg.value = ''
  loading.value = true
  try {
    await loanStore.create({
      equipment_id: form.value.equipment_id,
      borrower_user_id: form.value.borrower_user_id,
      loan_date: form.value.loan_date,
    })
    successMsg.value = '貸出を登録しました'
    form.value = { equipment_id: null, borrower_user_id: null, loan_date: today }
    await equipmentStore.fetchAll()
  } catch (e) {
    errorMsg.value = e.response?.data?.detail || '登録に失敗しました'
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await Promise.all([equipmentStore.fetchAll(), userStore.fetchAll()])
})
</script>
