<template>
  <v-app>
    <AppBar />
    <v-main>
      <v-container>
        <h2 class="mb-4">返却登録</h2>
        <v-snackbar v-model="snackbar" :color="snackbarColor" timeout="4000">{{ snackbarMessage }}</v-snackbar>
        <v-select
          v-model="selectedRecordId"
          :items="activeRecords"
          item-title="label"
          item-value="value"
          label="貸出記録"
          data-testid="return-record"
        />
        <v-text-field
          v-model="returnDate"
          label="返却日"
          type="date"
          data-testid="return-date"
        />
        <v-btn color="primary" @click="handleSubmit" data-testid="return-submit-button">登録</v-btn>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import AppBar from '@/components/AppBar.vue'
import { useLendingStore } from '@/stores/lending'
import { useItemStore } from '@/stores/item'

const router = useRouter()
const lendingStore = useLendingStore()
const itemStore = useItemStore()

const today = new Date().toISOString().slice(0, 10)
const selectedRecordId = ref(null)
const returnDate = ref(today)
const snackbar = ref(false)
const snackbarMessage = ref('')
const snackbarColor = ref('error')

const activeRecords = computed(() =>
  lendingStore.lendingRecords
    .filter((r) => !r.return_date)
    .map((r) => ({ label: `${r.borrower_name} / ${r.item_name}`, value: r.id }))
)

onMounted(async () => {
  await lendingStore.fetchLendingRecords()
})

async function handleSubmit() {
  try {
    await lendingStore.returnItem(selectedRecordId.value, { return_date: returnDate.value })
    await itemStore.fetchItems()
    router.push('/')
  } catch (e) {
    snackbarColor.value = 'error'
    snackbarMessage.value = e.response?.data?.detail || '登録に失敗しました'
    snackbar.value = true
  }
}
</script>
