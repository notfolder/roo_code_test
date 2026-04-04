<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="6" md="4">
        <v-card class="pa-6">
          <v-card-title class="text-h5 text-center mb-4">備品管理システム</v-card-title>
          <v-card-text>
            <v-form @submit.prevent="handleLogin">
              <v-text-field
                v-model="loginId"
                label="ログインID"
                required
                :error-messages="errors.loginId"
              />
              <v-text-field
                v-model="password"
                label="パスワード"
                type="password"
                required
                :error-messages="errors.password"
              />
              <v-alert v-if="errorMessage" type="error" class="mb-3">{{ errorMessage }}</v-alert>
              <v-btn type="submit" color="primary" block :loading="loading">ログイン</v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '../composables/useAuth.js'

const router = useRouter()
const { login } = useAuth()

const loginId = ref('')
const password = ref('')
const loading = ref(false)
const errorMessage = ref('')
const errors = ref({ loginId: '', password: '' })

async function handleLogin() {
  errors.value = { loginId: '', password: '' }
  errorMessage.value = ''

  // 未入力バリデーション
  if (!loginId.value) { errors.value.loginId = '入力してください'; return }
  if (!password.value) { errors.value.password = '入力してください'; return }

  loading.value = true
  try {
    await login(loginId.value, password.value)
    router.push({ name: 'equipment-list' })
  } catch (e) {
    errorMessage.value = e.response?.data?.detail || 'ログインに失敗しました'
  } finally {
    loading.value = false
  }
}
</script>
