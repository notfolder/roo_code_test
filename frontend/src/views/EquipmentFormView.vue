<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" sm="8" md="6">
        <v-card class="pa-4">
          <v-card-title>{{ isEdit ? '備品編集' : '備品登録' }}</v-card-title>
          <v-card-text>
            <v-form @submit.prevent="handleSubmit">
              <v-text-field
                v-if="!isEdit"
                v-model="form.code"
                label="管理番号"
                required
                :error-messages="errors.code"
              />
              <v-text-field
                v-else
                :model-value="form.code"
                label="管理番号"
                readonly
                disabled
              />
              <v-text-field
                v-model="form.name"
                label="備品名"
                required
                :error-messages="errors.name"
              />
              <v-alert v-if="errorMessage" type="error" class="mb-3">{{ errorMessage }}</v-alert>
              <v-row>
                <v-col><v-btn type="submit" color="primary" block :loading="loading">{{ isEdit ? '更新' : '登録' }}</v-btn></v-col>
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
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useEquipment } from '../composables/useEquipment.js'
import apiClient from '../api/client.js'

const router = useRouter()
const route = useRoute()
const { createEquipment, updateEquipment } = useEquipment()

const isEdit = computed(() => !!route.params.id)
const form = ref({ code: '', name: '' })
const errors = ref({ code: '', name: '' })
const errorMessage = ref('')
const loading = ref(false)

onMounted(async () => {
  if (isEdit.value) {
    // 編集時は既存データを取得して表示する
    const res = await apiClient.get('/api/equipments')
    const eq = res.data.find(e => e.id === Number(route.params.id))
    if (eq) { form.value.code = eq.code; form.value.name = eq.name }
  }
})

async function handleSubmit() {
  errors.value = { code: '', name: '' }
  errorMessage.value = ''

  if (!isEdit.value && !form.value.code.trim()) { errors.value.code = '入力してください'; return }
  if (!form.value.name.trim()) { errors.value.name = '入力してください'; return }

  loading.value = true
  try {
    if (isEdit.value) {
      await updateEquipment(Number(route.params.id), form.value.name)
    } else {
      await createEquipment(form.value.code, form.value.name)
    }
    router.push({ name: 'equipment-list' })
  } catch (e) {
    errorMessage.value = e.response?.data?.detail || '保存に失敗しました'
  } finally {
    loading.value = false
  }
}
</script>
