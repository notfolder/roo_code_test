<template>
  <AppLayout>
    <v-row>
      <v-col cols="12">
        <h1 class="text-h5 mb-4">ダッシュボード</h1>
      </v-col>
      <v-col cols="12" md="4">
        <v-card>
          <v-card-title>備品数</v-card-title>
          <v-card-text class="text-h3">{{ equipmentStore.items.length }}</v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="4">
        <v-card>
          <v-card-title>貸出中</v-card-title>
          <v-card-text class="text-h3 text-warning">{{ onLoanCount }}</v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="4">
        <v-card>
          <v-card-title>利用可能</v-card-title>
          <v-card-text class="text-h3 text-success">{{ availableCount }}</v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" class="mt-4">
        <v-card>
          <v-card-title>現在の貸出一覧</v-card-title>
          <v-data-table
            :headers="loanHeaders"
            :items="loanStore.activeLoans"
            :loading="loanStore.loading"
            no-data-text="貸出中の備品はありません"
          />
        </v-card>
      </v-col>
    </v-row>
  </AppLayout>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import AppLayout from './AppLayout.vue'
import { useEquipmentStore } from '../stores/equipment.js'
import { useLoanStore } from '../stores/loan.js'

const equipmentStore = useEquipmentStore()
const loanStore = useLoanStore()

const onLoanCount = computed(() => equipmentStore.items.filter((e) => e.status === 'on_loan').length)
const availableCount = computed(() => equipmentStore.items.filter((e) => e.status === 'available').length)

const loanHeaders = [
  { title: '備品名', key: 'equipment_name' },
  { title: '利用者', key: 'user_name' },
  { title: '貸出日', key: 'loan_date' },
  { title: '用途', key: 'purpose' },
]

onMounted(async () => {
  await Promise.all([equipmentStore.fetchAll(), loanStore.fetchActive()])
})
</script>
