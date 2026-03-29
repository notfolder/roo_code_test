<template>
  <AppLayout>
    <h1 class="text-h5 mb-4">返却登録</h1>

    <v-alert v-if="globalError" type="error" class="mb-4" closable @click:close="globalError = ''">
      {{ globalError }}
    </v-alert>

    <v-card>
      <v-data-table
        :headers="headers"
        :items="loanStore.activeLoans"
        :loading="loanStore.loading"
        no-data-text="現在貸出中の備品はありません"
      >
        <template #item.return_date="{ item }">
          <v-text-field
            v-model="returnDates[item.id]"
            type="date"
            density="compact"
            hide-details
            style="min-width: 160px"
          />
        </template>
        <template #item.actions="{ item }">
          <v-btn
            color="primary"
            size="small"
            :loading="processing[item.id]"
            :disabled="!returnDates[item.id]"
            @click="handleReturn(item.id)"
          >
            返却登録
          </v-btn>
        </template>
      </v-data-table>
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

const returnDates = ref({})
const processing = ref({})
const globalError = ref('')

const headers = [
  { title: '備品名', key: 'equipment_name' },
  { title: '借用者', key: 'user_name' },
  { title: '貸出日', key: 'loan_date' },
  { title: '返却日', key: 'return_date', sortable: false },
  { title: '操作', key: 'actions', sortable: false },
]

async function handleReturn(loanId) {
  globalError.value = ''
  processing.value[loanId] = true
  try {
    await loanStore.returnLoan(loanId, returnDates.value[loanId])
    delete returnDates.value[loanId]
    await equipmentStore.fetchAll()
  } catch (e) {
    globalError.value = e.response?.data?.detail || '登録に失敗しました'
  } finally {
    processing.value[loanId] = false
  }
}

onMounted(() => loanStore.fetchActive())
</script>
