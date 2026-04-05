<template>
  <v-container max-width="480">
    <v-card class="mt-8 pa-4">
      <v-card-title class="text-h5 mb-4">備品管理システム ログイン</v-card-title>
      <v-card-text>
        <v-text-field
          v-model="loginId"
          label="ログインID"
          variant="outlined"
          class="mb-2"
          data-testid="login-id"
        />
        <v-text-field
          v-model="password"
          label="パスワード"
          type="password"
          variant="outlined"
          class="mb-2"
          data-testid="login-password"
          @keyup.enter="handleLogin"
        />
        <v-alert v-if="errorMessage" type="error" class="mb-2">
          {{ errorMessage }}
        </v-alert>
      </v-card-text>
      <v-card-actions class="justify-center">
        <v-btn
          color="primary"
          :loading="loading"
          @click="handleLogin"
          data-testid="login-button"
        >
          ログイン
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { login } from '../api/client.js'
import { useAuthStore } from '../stores/auth.js'

const router = useRouter()
const authStore = useAuthStore()

const loginId = ref('')
const password = ref('')
const errorMessage = ref('')
const loading = ref(false)

async function handleLogin() {
  errorMessage.value = ''
  if (!loginId.value || !password.value) {
    errorMessage.value = 'IDとパスワードを入力してください'
    return
  }
  loading.value = true
  try {
    const response = await login(loginId.value, password.value)
    authStore.setToken(response.data.access_token)
    router.push('/')
  } catch (error) {
    errorMessage.value =
      error.response?.data?.detail || 'ログインに失敗しました'
  } finally {
    loading.value = false
  }
}
</script>
