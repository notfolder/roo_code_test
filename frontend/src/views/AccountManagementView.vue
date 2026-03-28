<template>
  <!-- アカウント管理画面（管理担当者専用） -->
  <v-container>
    <div class="d-flex align-center mb-4">
      <h2>アカウント管理</h2>
      <v-spacer />
      <v-btn color="primary" prepend-icon="mdi-plus" @click="createDialogOpen = true">
        アカウント作成
      </v-btn>
    </div>

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

    <!-- アカウント一覧テーブル -->
    <v-data-table
      :headers="headers"
      :items="accountStore.items"
      :loading="accountStore.loading"
      no-data-text="アカウントがありません"
      items-per-page="20"
    >
      <!-- 役割の日本語表示 -->
      <template v-slot:item.role="{ item }">
        {{ item.role === 'admin' ? '管理担当者' : '一般社員' }}
      </template>
      <!-- 作成日時のフォーマット -->
      <template v-slot:item.created_at="{ item }">
        {{ formatDate(item.created_at) }}
      </template>
      <!-- 削除ボタン -->
      <template v-slot:item.action="{ item }">
        <v-btn
          color="error"
          size="small"
          variant="text"
          icon="mdi-delete"
          @click="openDeleteDialog(item)"
        />
      </template>
    </v-data-table>

    <!-- アカウント作成ダイアログ -->
    <AccountFormDialog
      v-model="createDialogOpen"
      @submitted="handleCreate"
    />

    <!-- 削除確認ダイアログ -->
    <v-dialog v-model="deleteDialogOpen" max-width="400">
      <v-card>
        <v-card-title>削除確認</v-card-title>
        <v-card-text>
          <p>アカウント「<strong>{{ selectedAccount?.account_name }}</strong>」</p>
          <p>を削除してもよいですか？</p>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="deleteDialogOpen = false">キャンセル</v-btn>
          <v-btn color="error" :loading="deleteLoading" @click="handleDelete">削除</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAccountStore } from '../stores/account'
import AccountFormDialog from '../components/AccountFormDialog.vue'

const accountStore = useAccountStore()

const createDialogOpen = ref(false)
const deleteDialogOpen = ref(false)
const selectedAccount = ref(null)
const deleteLoading = ref(false)
const errorMessage = ref('')

// アカウント一覧テーブルのヘッダー定義
const headers = [
  { title: 'アカウント名', key: 'account_name', sortable: true },
  { title: '役割', key: 'role', sortable: true },
  { title: '作成日時', key: 'created_at', sortable: true },
  { title: '操作', key: 'action', sortable: false, align: 'center' },
]

onMounted(() => {
  accountStore.fetchAll()
})

/** 削除確認ダイアログを開く */
function openDeleteDialog(account) {
  selectedAccount.value = account
  deleteDialogOpen.value = true
}

/** アカウントを作成する */
async function handleCreate(data) {
  try {
    await accountStore.create(data)
  } catch (error) {
    errorMessage.value = error.response?.data?.detail ?? 'アカウントの作成に失敗しました'
  }
}

/** アカウントを削除する */
async function handleDelete() {
  deleteLoading.value = true
  try {
    await accountStore.remove(selectedAccount.value.id)
    deleteDialogOpen.value = false
  } catch (error) {
    errorMessage.value = error.response?.data?.detail ?? '削除に失敗しました'
    deleteDialogOpen.value = false
  } finally {
    deleteLoading.value = false
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
