<template>
  <v-app>
    <v-app-bar color="primary" flat>
      <v-app-bar-title>アカウント管理</v-app-bar-title>
      <v-spacer />
      <v-btn text @click="router.push('/')" data-testid="back-button">戻る</v-btn>
    </v-app-bar>
    <v-main>
      <v-container>
        <v-snackbar v-model="snackbar" :color="snackbarColor" timeout="4000">{{ snackbarMessage }}</v-snackbar>
        <div class="d-flex justify-end mb-4">
          <v-btn color="primary" @click="addDialog = true" data-testid="user-add-button">+ アカウント追加</v-btn>
        </div>
        <v-table>
          <thead>
            <tr>
              <th>ログインID</th>
              <th>ロール</th>
              <th>削除</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in userStore.users" :key="user.id">
              <td>{{ user.login_id }}</td>
              <td>{{ user.role === 'admin' ? '管理者' : '一般ユーザー' }}</td>
              <td>
                <v-btn size="small" color="error" @click="confirmDelete(user)" :data-testid="`user-delete-button-${user.id}`">削除</v-btn>
              </td>
            </tr>
          </tbody>
        </v-table>
      </v-container>
    </v-main>

    <UserFormDialog
      v-model="addDialog"
      @save="handleAddUser"
      @cancel="addDialog = false"
    />
    <ConfirmDialog
      v-model="confirmDialogVisible"
      title="アカウント削除"
      message="このアカウントを削除しますか？"
      @confirm="handleDelete"
      @cancel="confirmDialogVisible = false"
    />
  </v-app>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import UserFormDialog from '@/components/UserFormDialog.vue'
import ConfirmDialog from '@/components/ConfirmDialog.vue'

const router = useRouter()
const userStore = useUserStore()
const addDialog = ref(false)
const confirmDialogVisible = ref(false)
const deleteTarget = ref(null)
const snackbar = ref(false)
const snackbarMessage = ref('')
const snackbarColor = ref('error')

onMounted(() => userStore.fetchUsers())

async function handleAddUser(data) {
  try {
    await userStore.createUser(data)
    addDialog.value = false
    await userStore.fetchUsers()
    snackbarColor.value = 'success'
    snackbarMessage.value = 'ユーザーを追加しました'
    snackbar.value = true
  } catch (e) {
    snackbarColor.value = 'error'
    snackbarMessage.value = e.response?.data?.detail || '追加に失敗しました'
    snackbar.value = true
  }
}

function confirmDelete(user) {
  deleteTarget.value = user
  confirmDialogVisible.value = true
}

async function handleDelete() {
  confirmDialogVisible.value = false
  try {
    await userStore.deleteUser(deleteTarget.value.id)
    await userStore.fetchUsers()
    snackbarColor.value = 'success'
    snackbarMessage.value = '削除しました'
    snackbar.value = true
  } catch (e) {
    snackbarColor.value = 'error'
    snackbarMessage.value = e.response?.data?.detail || '削除に失敗しました'
    snackbar.value = true
  }
}
</script>
