<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import LoginForm from '../components/LoginForm.vue'
import api from '../services/api'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const errorMessage = ref('')

const login = async (form) => {
  errorMessage.value = ''
  try {
    const { data } = await api.post('/auth/login', form)
    authStore.setSession(data)
    router.push({ name: 'items' })
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || 'ログインに失敗しました'
  }
}
</script>

<template>
  <v-row justify="center" class="mt-12">
    <v-col cols="12" md="6" lg="5">
      <login-form @submit="login" />
      <v-alert v-if="errorMessage" type="error" variant="tonal" class="mt-4">{{ errorMessage }}</v-alert>
    </v-col>
  </v-row>
</template>
