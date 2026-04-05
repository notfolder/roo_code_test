<template>
  <v-container>
    <!-- ヘッダー -->
    <v-toolbar color="primary" dark flat class="mb-4 rounded">
      <v-toolbar-title>備品管理システム</v-toolbar-title>
      <v-spacer />
      <template v-if="authStore.isLoggedIn">
        <v-btn text @click="router.push('/lending/new')" data-testid="btn-lend">貸出</v-btn>
        <v-btn text @click="router.push('/lending/return')" data-testid="btn-return">返却</v-btn>
        <v-btn text @click="router.push('/equipment')" data-testid="btn-manage">備品管理</v-btn>
        <v-btn text @click="router.push('/lending/history')" data-testid="btn-history">履歴</v-btn>
        <v-btn text @click="handleLogout" data-testid="btn-logout">ログアウト</v-btn>
      </template>
      <template v-else>
        <v-btn text @click="router.push('/login')" data-testid="btn-login">ログイン</v-btn>
      </template>
    </v-toolbar>

    <!-- 備品一覧テーブル -->
    <v-card>
      <v-card-title>備品一覧</v-card-title>
      <v-data-table
        :headers="headers"
        :items="equipmentList"
        :loading="loading"
        no-data-text="備品が登録されていません"
        data-testid="equipment-table"
      >
        <template #item.status="{ item }">
          <v-chip :color="item.status === 'available' ? 'success' : 'warning'" size="small">
            {{ item.status === 'available' ? '利用可能' : '貸出中' }}
          </v-chip>
        </template>
        <template #item.borrower_name="{ item }">
          {{ item.borrower_name || '' }}
        </template>
      </v-data-table>
    </v-card>

    <v-snackbar v-model="snackbar" :color="snackbarColor" timeout="3000">
      {{ snackbarMessage }}
    </v-snackbar>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getEquipmentList } from '../api/client.js'
import { useAuthStore } from '../stores/auth.js'

const router = useRouter()
const authStore = useAuthStore()

const equipmentList = ref([])
const loading = ref(false)
const snackbar = ref(false)
const snackbarMessage = ref('')
const snackbarColor = ref('success')

const headers = [
  { title: '管理番号', key: 'management_number' },
  { title: '備品名', key: 'name' },
  { title: '種別', key: 'equipment_type' },
  { title: '状態', key: 'status' },
  { title: '借用者', key: 'borrower_name' },
]

async function fetchEquipmentList() {
  loading.value = true
  try {
    const response = await getEquipmentList()
    equipmentList.value = response.data
  } catch {
    showSnackbar('備品一覧の取得に失敗しました', 'error')
  } finally {
    loading.value = false
  }
}

function handleLogout() {
  authStore.logout()
  router.push('/')
}

function showSnackbar(message, color = 'success') {
  snackbarMessage.value = message
  snackbarColor.value = color
  snackbar.value = true
}

onMounted(fetchEquipmentList)
</script>
