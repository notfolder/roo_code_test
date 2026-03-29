<template>
  <AppLayout>
    <div class="d-flex align-center mb-4">
      <h1 class="text-h5">ユーザー管理</h1>
      <v-spacer />
      <v-btn color="primary" to="/users/create" prepend-icon="mdi-plus">ユーザー登録</v-btn>
    </div>
    <v-card>
      <v-data-table
        :headers="headers"
        :items="userStore.users"
        :loading="userStore.loading"
        no-data-text="ユーザーが登録されていません"
      >
        <template #item.role="{ item }">
          <v-chip :color="item.role === 'admin' ? 'primary' : 'default'" size="small">
            {{ item.role === 'admin' ? '管理者' : '一般' }}
          </v-chip>
        </template>
        <template #item.is_active="{ item }">
          <v-chip :color="item.is_active ? 'success' : 'error'" size="small">
            {{ item.is_active ? '有効' : '無効' }}
          </v-chip>
        </template>
        <template #item.actions="{ item }">
          <v-btn icon size="small" variant="text" color="error" @click="confirmDelete(item)">
            <v-icon>mdi-delete</v-icon>
          </v-btn>
        </template>
      </v-data-table>
    </v-card>

    <v-dialog v-model="deleteDialog" max-width="400">
      <v-card>
        <v-card-title>削除確認</v-card-title>
        <v-card-text>「{{ deleteTarget?.name }}」を削除しますか？</v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn @click="deleteDialog = false">キャンセル</v-btn>
          <v-btn color="error" :loading="deleting" @click="handleDelete">削除</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </AppLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import AppLayout from './AppLayout.vue'
import { useUserStore } from '../stores/user.js'

const userStore = useUserStore()

const deleteDialog = ref(false)
const deleteTarget = ref(null)
const deleting = ref(false)

const headers = [
  { title: 'ログインID', key: 'login_id' },
  { title: '氏名', key: 'name' },
  { title: '権限', key: 'role' },
  { title: 'ステータス', key: 'is_active' },
  { title: '操作', key: 'actions', sortable: false },
]

function confirmDelete(item) {
  deleteTarget.value = item
  deleteDialog.value = true
}

async function handleDelete() {
  deleting.value = true
  try {
    await userStore.remove(deleteTarget.value.id)
    deleteDialog.value = false
  } catch (e) {
    alert(e.response?.data?.detail || '削除に失敗しました')
  } finally {
    deleting.value = false
  }
}

onMounted(() => userStore.fetchAll())
</script>
