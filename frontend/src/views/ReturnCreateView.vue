<template>
  <AppLayout>
    <h1 class="text-h5 mb-4">返却登録</h1>
    <v-card class="pa-4" max-width="600">
      <v-form @submit.prevent="handleSubmit">
        <v-select
          v-model="selectedLoan"
          :items="loanStore.activeLoans"
          :item-title="(l) => `${l.equipment_name} (${l.user_name})`"
          item-value="id"
          label="貸出中の備品"
          required
        />
        <v-text-field v-model="returnDate" label="返却日" type="date" required />
        <v-alert v-if="errorMsg" type="error" class="mb-3">{{ errorMsg }}</v-alert>
        <v-alert v-if="successMsg" type="success" class="mb-3">{{ successMsg }}</v-alert>
        <div class="d-flex gap-2">
          <v-btn type="submit" color="primary" :loading="loading">返却登録</v-btn>
          <v-btn variant="text" to="/">キャンセル</v-btn>
        </div>
      </v-form>
    </v-card>
  </AppLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import AppLayout from './AppLayout.vue'
import { useLoanStore } from '../stores/loan.js'
import { useEquipmentStore } from '../stores/equipment.js'

const loanStore = useLoanStore()
const equipmentStore = useEquipmentStore()

const selectedLoan = ref(null)
const returnDate = ref(new Date().toISOString().split('T')[0])
const loading = ref(false)
const errorMsg = ref('')
const successMsg = ref('')

async function handleSubmit() {
  errorMsg.value = ''
  successMsg.value = ''
  loading.value = true
  try {
    await loanStore.returnLoan(selectedLoan.value, returnDate.value)
    successMsg.value = '返却を登録しました'
    selectedLoan.value = null
    await equipmentStore.fetchAll()
  } catch (e) {
    errorMsg.value = e.response?.data?.detail || '登録に失敗しました'
  } finally {
    loading.value = false
  }
}

onMounted(() => loanStore.fetchActive())
</script>
