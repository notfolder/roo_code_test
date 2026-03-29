<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card class="pa-4">
          <v-card-title class="text-h5 text-center mb-4">備品管理システム</v-card-title>
          <v-card-text>
            <v-form @submit.prevent="handleLogin">
              <v-text-field
                v-model="loginId"
                label="ログインID"
                prepend-icon="mdi-account"
                required
              />
              <v-text-field
                v-model="password"
                label="パスワード"
                type="password"
                prepend-icon="mdi-lock"
                required
              />
              <v-alert v-if="errorMsg" type="error" class="mb-3">{{ errorMsg }}</v-alert>
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
import { useAuthStore } from '../stores/auth.js'

const router = useRouter()
const auth = useAuthStore()

const loginId = ref('')
const password = ref('')
const loading = ref(false)
const errorMsg = ref('')

async function handleLogin() {
  errorMsg.value = ''
  loading.value = true
  try {
    await auth.login(loginId.value, password.value)
    router.push('/')
  } catch (e) {
    errorMsg.value = e.response?.data?.detail || 'ログインに失敗しました'
  } finally {
    loading.value = false
  }
}
</script>
