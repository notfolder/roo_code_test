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
        <v-select
          v-model="form.user_id"
          :items="userStore.users"
          item-title="name"
          item-value="id"
          label="利用者"
          required
        />
        <v-text-field v-model="form.loan_date" label="貸出日" type="date" required />
        <v-text-field v-model="form.purpose" label="用途" />
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
import { ref, computed, onMounted } from 'vue'
import AppLayout from './AppLayout.vue'
import { useEquipmentStore } from '../stores/equipment.js'
import { useUserStore } from '../stores/user.js'
import { useLoanStore } from '../stores/loan.js'

const equipmentStore = useEquipmentStore()
const userStore = useUserStore()
const loanStore = useLoanStore()

const loading = ref(false)
const errorMsg = ref('')
const successMsg = ref('')

const today = new Date().toISOString().split('T')[0]
const form = ref({ equipment_id: null, user_id: null, loan_date: today, purpose: '' })

const availableEquipment = computed(() => equipmentStore.items.filter((e) => e.status === 'available'))

async function handleSubmit() {
  errorMsg.value = ''
  successMsg.value = ''
  loading.value = true
  try {
    await loanStore.create({
      equipment_id: form.value.equipment_id,
      user_id: form.value.user_id,
      loan_date: form.value.loan_date,
      purpose: form.value.purpose || undefined,
    })
    successMsg.value = '貸出を登録しました'
    form.value = { equipment_id: null, user_id: null, loan_date: today, purpose: '' }
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
