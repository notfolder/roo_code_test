<template>
  <v-app>
    <v-main>
      <v-container>
        <div class="d-flex justify-space-between align-center mb-4">
          <div class="text-h6">アカウント管理</div>
          <v-btn color="primary" @click="fetchUsers">再読込</v-btn>
        </div>
        <v-card outlined class="mb-4">
          <v-card-title>ユーザー作成</v-card-title>
          <v-card-text>
            <v-form @submit.prevent="create">
              <v-text-field v-model="email" label="メール" required></v-text-field>
              <v-text-field v-model="name" label="氏名" required></v-text-field>
              <v-select :items="roles" v-model="role" label="ロール" required></v-select>
              <v-text-field v-model="password" label="パスワード" type="password" required></v-text-field>
              <v-btn type="submit" color="primary" class="mt-2">作成</v-btn>
              <div class="error" v-if="error">{{ error }}</div>
            </v-form>
          </v-card-text>
        </v-card>
        <v-simple-table>
          <thead>
            <tr>
              <th>メール</th>
              <th>氏名</th>
              <th>ロール</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="u in users" :key="u.id">
              <td>{{ u.email }}</td>
              <td>{{ u.name }}</td>
              <td>{{ u.role }}</td>
            </tr>
          </tbody>
        </v-simple-table>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'

const users = ref([])
const roles = ['general', 'admin']
const email = ref('')
const name = ref('')
const role = ref('general')
const password = ref('')
const error = ref('')

const fetchUsers = async () => {
  const res = await api.get('/users')
  users.value = res.data
}

const create = async () => {
  error.value = ''
  try {
    await api.post('/auth/users', { email: email.value, name: name.value, role: role.value, password: password.value })
    await fetchUsers()
  } catch (e) {
    error.value = '作成に失敗しました'
  }
}

onMounted(fetchUsers)
</script>

<style scoped>
.error { color: red; }
</style>
