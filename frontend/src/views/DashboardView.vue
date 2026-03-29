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
        <div class="d-flex gap-2 mb-3">
          <v-btn color="secondary" to="/reservations">予約一覧</v-btn>
          <v-btn color="secondary" to="/reservations/create">予約登録</v-btn>
        </div>
      </v-col>
      <v-col cols="12">
        <v-card>
          <v-card-title>備品一覧</v-card-title>
          <v-data-table
            :headers="equipmentHeaders"
            :items="equipmentRows"
            :loading="equipmentStore.loading || loanStore.loading"
            no-data-text="備品が登録されていません"
          >
            <template #item.status="{ item }">
              <v-chip :color="item.status === 'available' ? 'success' : 'warning'" size="small">
                {{ item.status === 'available' ? '貸出可' : '貸出中' }}
              </v-chip>
            </template>
          </v-data-table>
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

const onLoanCount = computed(() => equipmentStore.items.filter((e) => e.status === 'loaned').length)
const availableCount = computed(() => equipmentStore.items.filter((e) => e.status === 'available').length)

const equipmentHeaders = [
  { title: '備品名', key: 'name' },
  { title: '状態', key: 'status' },
  { title: '借用者', key: 'borrower' },
  { title: '貸出日', key: 'loan_date' },
]

const equipmentRows = computed(() =>
  equipmentStore.items.map((eq) => {
    const loan = loanStore.activeLoans.find((l) => l.equipment_id === eq.id)
    return {
      ...eq,
      borrower: loan ? loan.user_name : '—',
      loan_date: loan ? loan.loan_date : '—',
    }
  }),
)

onMounted(async () => {
  await Promise.all([equipmentStore.fetchAll(), loanStore.fetchActive()])
})
</script>
