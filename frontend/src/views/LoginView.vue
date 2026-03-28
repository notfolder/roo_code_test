<template>
  <!-- ログイン画面 -->
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card elevation="4">
          <v-card-title class="text-center pa-6 text-h6">
            社内備品管理・貸出管理システム
          </v-card-title>
          <v-card-text>
            <!-- エラーメッセージ -->
            <v-alert v-if="errorMessage" type="error" class="mb-4" density="compact">
              {{ errorMessage }}
            </v-alert>
            <v-text-field
              v-model="accountName"
              label="アカウント名"
              prepend-inner-icon="mdi-account"
              @keyup.enter="handleLogin"
            />
            <v-text-field
              v-model="password"
              label="パスワード"
              type="password"
              prepend-inner-icon="mdi-lock"
              @keyup.enter="handleLogin"
            />
          </v-card-text>
          <v-card-actions class="pa-4">
            <v-btn
              color="primary"
              block
              size="large"
              :loading="loading"
              @click="handleLogin"
            >
              ログイン
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const accountName = ref('')
const password = ref('')
const loading = ref(false)
const errorMessage = ref('')

/** ログイン処理：認証成功後にトップページに遷移する */
async function handleLogin() {
  if (!accountName.value || !password.value) {
    errorMessage.value = 'アカウント名とパスワードを入力してください'
    return
  }
  loading.value = true
  errorMessage.value = ''
  try {
    await authStore.login(accountName.value, password.value)
    router.push('/')
  } catch (error) {
    const detail = error.response?.data?.detail
    errorMessage.value = detail ?? 'ログインに失敗しました'
  } finally {
    loading.value = false
  }
}
</script>
