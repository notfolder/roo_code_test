<template>
  <AppLayout>
    <h1 class="text-h5 mb-4">予約登録</h1>
    <v-card class="pa-4" max-width="600">
      <v-form @submit.prevent="handleSubmit">
        <v-select
          v-model="form.equipment_id"
          :items="equipmentStore.items"
          item-title="name"
          item-value="id"
          label="備品"
          hint="全備品から選択できます"
          persistent-hint
          required
        />
        <v-text-field
          v-model="form.planned_start_date"
          label="貸出開始予定日"
          type="date"
          :min="today"
          required
          class="mt-3"
        />
        <v-text-field
          v-model="form.planned_return_date"
          label="返却予定日"
          type="date"
          :min="form.planned_start_date || today"
          required
          class="mt-3"
        />
        <v-alert type="info" variant="tonal" class="mt-3 mb-3" density="compact">
          予約期間が他の予約と重複する場合は登録できません。貸出開始予定日は本日以降を入力してください。
        </v-alert>
        <v-alert v-if="errorMsg" type="error" class="mb-3">{{ errorMsg }}</v-alert>
        <v-alert v-if="successMsg" type="success" class="mb-3">{{ successMsg }}</v-alert>
        <div class="d-flex gap-2">
          <v-btn type="submit" color="primary" :loading="loading">予約する</v-btn>
          <v-btn variant="text" to="/reservations">キャンセル</v-btn>
        </div>
      </v-form>
    </v-card>
  </AppLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import AppLayout from './AppLayout.vue'
import { useEquipmentStore } from '../stores/equipment.js'
import { useReservationStore } from '../stores/reservation.js'

const equipmentStore = useEquipmentStore()
const reservationStore = useReservationStore()
const router = useRouter()

const loading = ref(false)
const errorMsg = ref('')
const successMsg = ref('')

const today = new Date().toISOString().split('T')[0]
const form = ref({ equipment_id: null, planned_start_date: today, planned_return_date: today })

async function handleSubmit() {
  errorMsg.value = ''
  successMsg.value = ''
  loading.value = true
  try {
    await reservationStore.createReservation({
      equipment_id: form.value.equipment_id,
      planned_start_date: form.value.planned_start_date,
      planned_return_date: form.value.planned_return_date,
    })
    router.push('/reservations')
  } catch (e) {
    errorMsg.value = e.response?.data?.detail || '予約登録に失敗しました'
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await equipmentStore.fetchAll()
})
</script>
