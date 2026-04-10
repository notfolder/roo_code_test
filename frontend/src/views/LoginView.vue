<template>
  <v-container class="fill-height" fluid>
    <v-row justify="center" align="center">
      <v-col cols="12" sm="6" md="4">
        <v-card>
          <v-card-title class="text-center pt-6">備品管理システム</v-card-title>
          <v-card-text>
            <v-text-field
              v-model="loginId"
              label="ログインID"
              data-testid="login-id"
            />
            <v-text-field
              v-model="password"
              label="パスワード"
              type="password"
              data-testid="login-password"
            />
            <v-alert v-if="errorMessage" type="error" class="mt-2">
              {{ errorMessage }}
            </v-alert>
          </v-card-text>
          <v-card-actions class="justify-center pb-6">
            <v-btn
              color="primary"
              @click="handleLogin"
              data-testid="login-button"
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
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const loginId = ref('')
const password = ref('')
const errorMessage = ref('')

async function handleLogin() {
  errorMessage.value = ''
  try {
    await authStore.login(loginId.value, password.value)
    router.push('/')
  } catch {
    errorMessage.value = 'IDまたはパスワードが正しくありません'
  }
}
</script>
