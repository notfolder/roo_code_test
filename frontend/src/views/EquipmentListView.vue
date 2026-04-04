<template>
  <v-app-bar color="primary" flat>
    <v-app-bar-title>備品管理システム</v-app-bar-title>
    <template #append>
      <v-btn v-if="isAdmin" variant="text" @click="router.push({ name: 'user-list' })">ユーザー管理</v-btn>
      <span class="mr-3">{{ username }}</span>
      <v-btn variant="text" @click="handleLogout">ログアウト</v-btn>
    </template>
  </v-app-bar>

  <v-main>
    <v-container>
      <v-row class="mb-3" align="center">
        <v-col><span class="text-h6">備品一覧</span></v-col>
        <v-col cols="auto">
          <v-btn v-if="isAdmin" color="primary" @click="router.push({ name: 'equipment-create' })">+ 備品登録</v-btn>
        </v-col>
      </v-row>

      <v-alert v-if="error" type="error" class="mb-3">{{ error }}</v-alert>

      <v-table>
        <thead>
          <tr>
            <th>管理番号</th>
            <th>備品名</th>
            <th>状態</th>
            <th>借用者</th>
            <th v-if="isAdmin">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="eq in equipments" :key="eq.id">
            <td>{{ eq.code }}</td>
            <td>{{ eq.name }}</td>
            <td>
              <v-chip :color="eq.status === 'available' ? 'success' : 'warning'" size="small">
                {{ eq.status === 'available' ? '在庫あり' : '貸出中' }}
              </v-chip>
            </td>
            <td>{{ eq.borrower_name || '' }}</td>
            <td v-if="isAdmin">
              <v-btn size="small" variant="text" @click="router.push({ name: 'equipment-edit', params: { id: eq.id } })">編集</v-btn>
              <v-btn
                size="small"
                variant="text"
                color="error"
                :disabled="eq.status === 'lending'"
                @click="handleDelete(eq)"
              >削除</v-btn>
              <v-btn
                size="small"
                variant="text"
                color="primary"
                :disabled="eq.status === 'lending'"
                @click="router.push({ name: 'equipment-lend', params: { id: eq.id } })"
              >貸出</v-btn>
              <v-btn
                size="small"
                variant="text"
                color="secondary"
                :disabled="eq.status === 'available'"
                @click="router.push({ name: 'equipment-return', params: { id: eq.id } })"
              >返却</v-btn>
            </td>
          </tr>
        </tbody>
      </v-table>
    </v-container>
  </v-main>

  <!-- 削除確認ダイアログ -->
  <v-dialog v-model="deleteDialog" max-width="400">
    <v-card>
      <v-card-title>削除確認</v-card-title>
      <v-card-text>「{{ deleteTarget?.name }}」を削除しますか？</v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn @click="deleteDialog = false">キャンセル</v-btn>
        <v-btn color="error" @click="confirmDelete">削除</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <v-snackbar v-model="snackbar.show" :color="snackbar.color">{{ snackbar.message }}</v-snackbar>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '../composables/useAuth.js'
import { useEquipment } from '../composables/useEquipment.js'

const router = useRouter()
const { isAdmin, username, logout } = useAuth()
const { equipments, error, fetchEquipments, deleteEquipment } = useEquipment()

const deleteDialog = ref(false)
const deleteTarget = ref(null)
const snackbar = ref({ show: false, message: '', color: 'success' })

onMounted(fetchEquipments)

function handleLogout() {
  logout()
  router.push({ name: 'login' })
}

function handleDelete(eq) {
  deleteTarget.value = eq
  deleteDialog.value = true
}

async function confirmDelete() {
  deleteDialog.value = false
  try {
    await deleteEquipment(deleteTarget.value.id)
    snackbar.value = { show: true, message: '削除しました', color: 'success' }
    await fetchEquipments()
  } catch (e) {
    snackbar.value = { show: true, message: e.response?.data?.detail || '削除に失敗しました', color: 'error' }
  }
}
</script>
