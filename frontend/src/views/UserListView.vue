<template>
  <v-app-bar color="primary" flat>
    <v-app-bar-title>ユーザー管理</v-app-bar-title>
    <template #append>
      <v-btn variant="text" @click="router.push({ name: 'equipment-list' })">備品一覧へ</v-btn>
    </template>
  </v-app-bar>

  <v-main>
    <v-container>
      <v-row class="mb-3" align="center">
        <v-col><span class="text-h6">ユーザー一覧</span></v-col>
        <v-col cols="auto">
          <v-btn color="primary" @click="router.push({ name: 'user-create' })">+ ユーザー登録</v-btn>
        </v-col>
      </v-row>

      <v-alert v-if="error" type="error" class="mb-3">{{ error }}</v-alert>

      <v-table>
        <thead>
          <tr>
            <th>ユーザー名</th>
            <th>ログインID</th>
            <th>ロール</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="u in users" :key="u.id">
            <td>{{ u.username }}</td>
            <td>{{ u.login_id }}</td>
            <td>{{ u.role === 'admin' ? '総務担当者' : '一般社員' }}</td>
            <td>
              <v-btn size="small" variant="text" @click="router.push({ name: 'user-edit', params: { id: u.id } })">編集</v-btn>
              <v-btn
                size="small"
                variant="text"
                color="error"
                :disabled="u.id === currentUserId"
                @click="handleDelete(u)"
              >削除</v-btn>
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
      <v-card-text>「{{ deleteTarget?.username }}」を削除しますか？</v-card-text>
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
import { useUser } from '../composables/useUser.js'
import { jwtDecode } from 'jwt-decode'

const router = useRouter()
const { users, error, fetchUsers, deleteUser } = useUser()

const deleteDialog = ref(false)
const deleteTarget = ref(null)
const snackbar = ref({ show: false, message: '', color: 'success' })

// 自分自身のIDを取得（自己削除ボタンを非活性にするため）
const currentUserId = ref(null)
onMounted(async () => {
  const token = localStorage.getItem('access_token')
  if (token) {
    try {
      const payload = jwtDecode(token)
      currentUserId.value = Number(payload.sub)
    } catch {}
  }
  await fetchUsers()
})

function handleDelete(u) {
  deleteTarget.value = u
  deleteDialog.value = true
}

async function confirmDelete() {
  deleteDialog.value = false
  try {
    await deleteUser(deleteTarget.value.id)
    snackbar.value = { show: true, message: '削除しました', color: 'success' }
    await fetchUsers()
  } catch (e) {
    snackbar.value = { show: true, message: e.response?.data?.detail || '削除に失敗しました', color: 'error' }
  }
}
</script>
