<template>
  <!-- 貸出・返却管理画面（管理担当者専用） -->
  <v-container>
    <h2 class="mb-4">貸出・返却管理</h2>

    <!-- エラーメッセージ -->
    <v-alert
      v-if="errorMessage"
      type="error"
      class="mb-4"
      density="compact"
      closable
      @click:close="errorMessage = ''"
    >
      {{ errorMessage }}
    </v-alert>

    <!-- 備品一覧テーブル（貸出・返却操作付き） -->
    <EquipmentTable
      :items="equipmentStore.items"
      :loading="equipmentStore.loading"
      :show-status="true"
      :show-loan-actions="true"
      :show-borrower="true"
      :active-loan-map="activeLoanMap"
      @loan-click="openLoanDialog"
      @return-click="openReturnDialog"
    />

    <!-- 貸出履歴テーブル -->
    <h3 class="mt-8 mb-4">貸出履歴</h3>
    <v-data-table
      :headers="historyHeaders"
      :items="loanStore.items"
      :loading="loanStore.loading"
      no-data-text="貸出履歴がありません"
      items-per-page="20"
    >
      <template v-slot:item.loaned_at="{ item }">
        {{ formatDate(item.loaned_at) }}
      </template>
      <template v-slot:item.returned_at="{ item }">
        {{ item.returned_at ? formatDate(item.returned_at) : '—' }}
      </template>
    </v-data-table>

    <!-- 貸出ダイアログ -->
    <LoanDialog
      v-model="loanDialogOpen"
      :equipment="selectedEquipment"
      @submitted="handleLoanSubmit"
    />

    <!-- 返却ダイアログ -->
    <ReturnDialog
      v-model="returnDialogOpen"
      :equipment="selectedEquipment"
      :active-loan="selectedActiveLoan"
      @submitted="handleReturnSubmit"
    />
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useEquipmentStore } from '../stores/equipment'
import { useLoanStore } from '../stores/loan'
import EquipmentTable from '../components/EquipmentTable.vue'
import LoanDialog from '../components/LoanDialog.vue'
import ReturnDialog from '../components/ReturnDialog.vue'

const equipmentStore = useEquipmentStore()
const loanStore = useLoanStore()

const loanDialogOpen = ref(false)
const returnDialogOpen = ref(false)
const selectedEquipment = ref(null)
const selectedActiveLoan = ref(null)
const errorMessage = ref('')

// 貸出履歴テーブルのヘッダー定義
const historyHeaders = [
  { title: '管理番号', key: 'management_number', sortable: true },
  { title: '備品名', key: 'equipment_name', sortable: true },
  { title: '借用者', key: 'borrower_name', sortable: true },
  { title: '貸出日時', key: 'loaned_at', sortable: true },
  { title: '返却日時', key: 'returned_at', sortable: true },
  { title: '操作担当', key: 'operator_name', sortable: false },
]

/** 貸出中備品のloan情報マップ（equipment_id → LoanRecord）を生成する */
const activeLoanMap = computed(() => {
  const map = {}
  loanStore.items
    .filter((l) => l.returned_at === null)
    .forEach((l) => { map[l.equipment_id] = l })
  return map
})

onMounted(async () => {
  await Promise.all([
    equipmentStore.fetchAll(false),
    loanStore.fetchAll(),
  ])
})

/** 貸出ダイアログを開く */
function openLoanDialog(equipment) {
  selectedEquipment.value = equipment
  loanDialogOpen.value = true
}

/** 返却ダイアログを開く */
function openReturnDialog(equipment) {
  selectedEquipment.value = equipment
  selectedActiveLoan.value = activeLoanMap.value[equipment.id] ?? null
  returnDialogOpen.value = true
}

/** 貸出を実行する */
async function handleLoanSubmit({ equipmentId, borrowerAccountId }) {
  try {
    await loanStore.create(equipmentId, borrowerAccountId)
    // 貸出後に備品の状態を更新するため再取得する
    await equipmentStore.fetchAll(false)
  } catch (error) {
    errorMessage.value = error.response?.data?.detail ?? '貸出の登録に失敗しました'
  }
}

/** 返却を実行する */
async function handleReturnSubmit({ loanId }) {
  try {
    await loanStore.returnLoan(loanId)
    // 返却後に備品の状態を更新するため再取得する
    await equipmentStore.fetchAll(false)
  } catch (error) {
    errorMessage.value = error.response?.data?.detail ?? '返却の登録に失敗しました'
  }
}

/** 日時を日本語形式にフォーマットする */
function formatDate(dateStr) {
  return new Date(dateStr).toLocaleString('ja-JP', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })
}
</script>
