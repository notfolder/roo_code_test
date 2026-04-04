<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" sm="8" md="6">
        <v-card class="pa-4">
          <v-card-title>{{ isEdit ? 'ユーザー編集' : 'ユーザー登録' }}</v-card-title>
          <v-card-text>
            <v-form @submit.prevent="handleSubmit">
              <v-text-field
                v-if="!isEdit"
                v-model="form.loginId"
                label="ログインID"
                required
                :error-messages="errors.loginId"
              />
              <v-text-field
                v-else
                :model-value="form.loginId"
                label="ログインID"
                readonly
                disabled
              />
              <v-text-field
                v-model="form.username"
                label="ユーザー名"
                required
                :error-messages="errors.username"
              />
              <v-text-field
                v-if="!isEdit"
                v-model="form.password"
                label="パスワード"
                type="password"
                required
                :error-messages="errors.password"
              />
              <v-select
                v-model="form.role"
                :items="roleItems"
                item-title="label"
                item-value="value"
                label="ロール"
                required
                :error-messages="errors.role"
              />
              <v-alert v-if="errorMessage" type="error" class="mb-3">{{ errorMessage }}</v-alert>
              <v-row>
                <v-col><v-btn type="submit" color="primary" block :loading="loading">{{ isEdit ? '更新' : '登録' }}</v-btn></v-col>
                <v-col><v-btn block @click="router.push({ name: 'user-list' })">キャンセル</v-btn></v-col>
              </v-row>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUser } from '../composables/useUser.js'
import apiClient from '../api/client.js'

const router = useRouter()
const route = useRoute()
const { createUser, updateUser } = useUser()

const isEdit = computed(() => !!route.params.id)
const form = ref({ loginId: '', username: '', password: '', role: 'staff' })
const errors = ref({ loginId: '', username: '', password: '', role: '' })
const errorMessage = ref('')
const loading = ref(false)

const roleItems = [
  { label: '総務担当者', value: 'admin' },
  { label: '一般社員', value: 'staff' },
]

onMounted(async () => {
  if (isEdit.value) {
    const res = await apiClient.get('/api/users')
    const u = res.data.find(u => u.id === Number(route.params.id))
    if (u) { form.value.loginId = u.login_id; form.value.username = u.username; form.value.role = u.role }
  }
})

async function handleSubmit() {
  errors.value = { loginId: '', username: '', password: '', role: '' }
  errorMessage.value = ''

  if (!isEdit.value && !form.value.loginId.trim()) { errors.value.loginId = '入力してください'; return }
  if (!form.value.username.trim()) { errors.value.username = '入力してください'; return }
  if (!isEdit.value && !form.value.password) { errors.value.password = '入力してください'; return }

  loading.value = true
  try {
    if (isEdit.value) {
      await updateUser(Number(route.params.id), form.value.username, form.value.role)
    } else {
      await createUser(form.value.loginId, form.value.username, form.value.password, form.value.role)
    }
    router.push({ name: 'user-list' })
  } catch (e) {
    errorMessage.value = e.response?.data?.detail || '保存に失敗しました'
  } finally {
    loading.value = false
  }
}
</script>
