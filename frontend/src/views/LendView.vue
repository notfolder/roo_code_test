<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" sm="8" md="6">
        <v-card class="pa-4">
          <v-card-title>貸出登録</v-card-title>
          <v-card-text>
            <v-form @submit.prevent="handleSubmit">
              <v-text-field :model-value="equipment?.code" label="管理番号" readonly disabled />
              <v-text-field :model-value="equipment?.name" label="備品名" readonly disabled />
              <v-text-field
                v-model="borrowerName"
                label="借用者名"
                required
                :error-messages="errors.borrowerName"
              />
              <v-alert v-if="errorMessage" type="error" class="mb-3">{{ errorMessage }}</v-alert>
              <v-row>
                <v-col><v-btn type="submit" color="primary" block :loading="loading">貸出登録</v-btn></v-col>
                <v-col><v-btn block @click="router.push({ name: 'equipment-list' })">キャンセル</v-btn></v-col>
              </v-row>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useEquipment } from '../composables/useEquipment.js'
import apiClient from '../api/client.js'

const router = useRouter()
const route = useRoute()
const { lendEquipment } = useEquipment()

const equipment = ref(null)
const borrowerName = ref('')
const errors = ref({ borrowerName: '' })
const errorMessage = ref('')
const loading = ref(false)

onMounted(async () => {
  const res = await apiClient.get('/api/equipments')
  equipment.value = res.data.find(e => e.id === Number(route.params.id))
})

async function handleSubmit() {
  errors.value = { borrowerName: '' }
  errorMessage.value = ''
  if (!borrowerName.value.trim()) { errors.value.borrowerName = '入力してください'; return }

  loading.value = true
  try {
    await lendEquipment(Number(route.params.id), borrowerName.value)
    router.push({ name: 'equipment-list' })
  } catch (e) {
    errorMessage.value = e.response?.data?.detail || '貸出登録に失敗しました'
  } finally {
    loading.value = false
  }
}
</script>
