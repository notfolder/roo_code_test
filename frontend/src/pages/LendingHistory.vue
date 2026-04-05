<template>
  <v-container>
    <v-toolbar color="primary" dark flat class="mb-4 rounded">
      <v-btn icon @click="router.push('/')"><v-icon>mdi-arrow-left</v-icon></v-btn>
      <v-toolbar-title>貸出履歴</v-toolbar-title>
    </v-toolbar>

    <v-card>
      <v-data-table
        :headers="headers"
        :items="historyList"
        :loading="loading"
        no-data-text="貸出履歴がありません"
        data-testid="lending-history-table"
      >
        <template #item.returned_at="{ item }">
          {{ item.returned_at || '未返却' }}
        </template>
      </v-data-table>
    </v-card>

    <v-snackbar v-model="snackbar" color="error" timeout="3000">
      {{ snackbarMessage }}
    </v-snackbar>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getLendingHistory } from '../api/client.js'

const router = useRouter()

const historyList = ref([])
const loading = ref(false)
const snackbar = ref(false)
const snackbarMessage = ref('')

const headers = [
  { title: '管理番号', key: 'management_number' },
  { title: '備品名', key: 'equipment_name' },
  { title: '借用者', key: 'borrower_name' },
  { title: '貸出日', key: 'lent_at' },
  { title: '返却日', key: 'returned_at' },
]

async function fetchHistory() {
  loading.value = true
  try {
    const response = await getLendingHistory()
    historyList.value = response.data
  } catch {
    snackbarMessage.value = '履歴の取得に失敗しました'
    snackbar.value = true
  } finally {
    loading.value = false
  }
}

onMounted(fetchHistory)
</script>
