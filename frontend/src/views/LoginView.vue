<template>
  <v-container class="ma-4" max-width="420">
    <v-card>
      <v-card-title>ログイン</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="onSubmit">
          <v-text-field v-model="email" label="メール" type="email" required density="comfortable" />
          <v-text-field v-model="password" label="パスワード" type="password" required density="comfortable" />
          <v-alert v-if="error" type="error" dense>{{ error }}</v-alert>
          <v-btn color="primary" type="submit" block :loading="loading">ログイン</v-btn>
        </v-form>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import axios from 'axios'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

const api = axios.create({ baseURL: import.meta.env.VITE_API_BASE || 'http://localhost:8000' })

const onSubmit = async () => {
  error.value = ''
  loading.value = true
  try {
    const res = await api.post('/auth/login', { email: email.value, password: password.value })
    const token = res.data.token
    localStorage.setItem('token', token)
    router.push('/equipments')
  } catch (e) {
    error.value = e.response?.data?.detail || '認証に失敗しました'
  } finally {
    loading.value = false
  }
}
</script>
