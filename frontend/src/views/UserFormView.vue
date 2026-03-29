<template>
  <AppLayout>
    <h1 class="text-h5 mb-4">ユーザー登録</h1>
    <v-card class="pa-4" max-width="600">
      <v-form @submit.prevent="handleSubmit">
        <v-text-field v-model="form.login_id" label="ログインID" required />
        <v-text-field v-model="form.name" label="氏名" required />
        <v-text-field v-model="form.password" label="パスワード" type="password" required />
        <v-select
          v-model="form.role"
          :items="[{ title: '一般', value: 'general' }, { title: '管理者', value: 'admin' }]"
          item-title="title"
          item-value="value"
          label="権限"
        />
        <v-alert v-if="errorMsg" type="error" class="mb-3">{{ errorMsg }}</v-alert>
        <div class="d-flex gap-2">
          <v-btn type="submit" color="primary" :loading="loading">登録</v-btn>
          <v-btn variant="text" to="/users">キャンセル</v-btn>
        </div>
      </v-form>
    </v-card>
  </AppLayout>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import AppLayout from './AppLayout.vue'
import { useUserStore } from '../stores/user.js'

const router = useRouter()
const userStore = useUserStore()

const loading = ref(false)
const errorMsg = ref('')
const form = ref({ login_id: '', name: '', password: '', role: 'general' })

async function handleSubmit() {
  errorMsg.value = ''
  loading.value = true
  try {
    await userStore.create(form.value)
    router.push('/users')
  } catch (e) {
    errorMsg.value = e.response?.data?.detail || '登録に失敗しました'
  } finally {
    loading.value = false
  }
}
</script>
