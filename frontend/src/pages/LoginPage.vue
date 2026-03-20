<template>
  <v-app>
    <v-main>
      <v-container class="d-flex justify-center align-center" style="height: 100vh;">
        <v-card width="420">
          <v-card-title class="text-h6">ログイン</v-card-title>
          <v-card-text>
            <v-form @submit.prevent="onSubmit">
              <v-text-field v-model="email" label="メール" type="email" required></v-text-field>
              <v-text-field v-model="password" label="パスワード" type="password" required></v-text-field>
              <v-btn type="submit" color="primary" block class="mt-4">ログイン</v-btn>
              <div class="error mt-2" v-if="error">{{ error }}</div>
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

const onSubmit = async () => {
  error.value = ''
  try {
    const res = await api.post('/auth/login', { email: email.value, password: password.value })
    const token = res.data.access_token
    localStorage.setItem('token', token)
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`
    router.push('/dashboard')
  } catch (e) {
    error.value = '認証に失敗しました'
  }
}
</script>

<style scoped>
.error {
  color: red;
}
</style>
