<script setup>
import { onMounted, ref } from 'vue'
import UserDetailDialog from '../components/UserDetailDialog.vue'
import UserFormDialog from '../components/UserFormDialog.vue'
import api from '../services/api'

const users = ref([])
const message = ref('')
const errorMessage = ref('')

const showFormDialog = ref(false)
const showDetailDialog = ref(false)
const selectedUser = ref(null)

const fetchUsers = async () => {
  const { data } = await api.get('/users')
  users.value = data
}

const load = async () => {
  try {
    await fetchUsers()
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || 'ユーザー取得に失敗しました'
  }
}

const openCreate = () => {
  selectedUser.value = null
  showFormDialog.value = true
}

const openEdit = (user) => {
  selectedUser.value = user
  showFormDialog.value = true
}

const openDetail = async (user) => {
  const { data } = await api.get(`/users/${user.id}`)
  selectedUser.value = data
  showDetailDialog.value = true
}

const saveUser = async (payload) => {
  message.value = ''
  errorMessage.value = ''
  try {
    if (selectedUser.value) {
      await api.put(`/users/${selectedUser.value.id}`, {
        email: payload.email,
        name: payload.name,
        role: payload.role
      })
      message.value = 'ユーザーを更新しました'
    } else {
      await api.post('/users', payload)
      message.value = 'ユーザーを登録しました'
    }
    showFormDialog.value = false
    await fetchUsers()
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || 'ユーザー保存に失敗しました'
  }
}

const deleteUser = async (user) => {
  message.value = ''
  errorMessage.value = ''
  try {
    await api.delete(`/users/${user.id}`)
    message.value = 'ユーザーを削除済みに変更しました'
    await fetchUsers()
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || 'ユーザー削除に失敗しました'
  }
}

onMounted(load)
</script>

<template>
  <v-card elevation="3">
    <v-card-title class="d-flex align-center">
      <span class="text-h6">ユーザー管理</span>
      <v-spacer />
      <v-btn color="primary" data-testid="create-user-button" @click="openCreate">ユーザー登録</v-btn>
    </v-card-title>
    <v-card-text>
      <v-alert v-if="message" type="success" variant="tonal" class="mb-4">{{ message }}</v-alert>
      <v-alert v-if="errorMessage" type="error" variant="tonal" class="mb-4">{{ errorMessage }}</v-alert>

      <v-table>
        <thead>
          <tr>
            <th>氏名</th>
            <th>メール</th>
            <th>ロール</th>
            <th>ステータス</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id" :data-testid="`user-row-${user.email}`">
            <td>{{ user.name }}</td>
            <td>{{ user.email }}</td>
            <td>{{ user.role === 'admin' ? '総務' : '社員' }}</td>
            <td>
              <v-chip :color="user.status === 'active' ? 'teal' : 'grey'" size="small" text-color="white">
                {{ user.status === 'active' ? '有効' : '削除済' }}
              </v-chip>
            </td>
            <td>
              <v-btn size="small" variant="text" class="mr-1" :data-testid="`user-detail-${user.email}`" @click="openDetail(user)">
                詳細
              </v-btn>
              <v-btn
                size="small"
                variant="text"
                color="primary"
                class="mr-1"
                :data-testid="`user-edit-${user.email}`"
                @click="openEdit(user)"
              >
                編集
              </v-btn>
              <v-btn
                size="small"
                variant="text"
                color="error"
                :data-testid="`user-delete-${user.email}`"
                @click="deleteUser(user)"
              >
                削除
              </v-btn>
            </td>
          </tr>
        </tbody>
      </v-table>
    </v-card-text>
  </v-card>

  <user-form-dialog v-model="showFormDialog" :user="selectedUser" @save="saveUser" />
  <user-detail-dialog v-model="showDetailDialog" :user="selectedUser" />
</template>
