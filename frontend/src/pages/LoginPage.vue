<template>
  <v-app>
    <v-main>
      <v-container class="d-flex justify-center align-center" style="height: 100vh;">
        <v-card width="420">
          <v-card-title class="text-h6">ログイン</v-card-title>
          <v-card-text>
            <v-form @submit.prevent="onSubmit">
              <!-- メールアドレス入力 -->
              <v-text-field
                v-model="email"
                label="メール"
                type="email"
                required
                prepend-icon="mdi-email"
                density="comfortable"
                variant="outlined"
              ></v-text-field>

              <!-- パスワード入力 -->
              <v-text-field
                v-model="password"
                label="パスワード"
                type="password"
                required
                prepend-icon="mdi-lock"
                density="comfortable"
                variant="outlined"
              ></v-text-field>

              <!-- ログインボタン -->
              <v-btn type="submit" color="primary" block class="mt-4" :loading="loading">
                ログイン
              </v-btn>

              <!-- エラー表示 -->
              <v-alert v-if="error" type="error" dense class="mt-3">{{ error }}</v-alert>
            </v-form>
          </v-card-text>
        </v-card>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

const router = useRouter()
const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

const onSubmit = async () => {
  error.value = ''
  loading.value = true
  try {
    const res = await api.post('/auth/login', { email: email.value, password: password.value })
    const token = res.data.access_token
    localStorage.setItem('token', token)
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`
    router.push('/dashboard')
  } catch (e) {
    error.value = '認証に失敗しました'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.error {
  color: red;
}
</style>
