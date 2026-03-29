<template>
  <AppLayout>
    <h1 class="text-h5 mb-4">{{ isEdit ? '備品編集' : '備品登録' }}</h1>
    <v-card class="pa-4" max-width="600">
      <v-form @submit.prevent="handleSubmit">
        <v-text-field v-model="form.name" label="備品名" required />
        <v-select
          v-model="form.category"
          :items="categories"
          label="カテゴリ"
          required
        />
        <v-text-field v-model="form.notes" label="備考" />
        <v-alert v-if="errorMsg" type="error" class="mb-3">{{ errorMsg }}</v-alert>
        <div class="d-flex gap-2">
          <v-btn type="submit" color="primary" :loading="loading">{{ isEdit ? '更新' : '登録' }}</v-btn>
          <v-btn variant="text" to="/equipment">キャンセル</v-btn>
        </div>
      </v-form>
    </v-card>
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AppLayout from './AppLayout.vue'
import { useEquipmentStore } from '../stores/equipment.js'

const route = useRoute()
const router = useRouter()
const equipmentStore = useEquipmentStore()

const isEdit = computed(() => !!route.params.id)
const loading = ref(false)
const errorMsg = ref('')

const categories = ['ノートPC', 'プロジェクター', '延長コード', 'カメラ', 'その他']
const form = ref({ name: '', category: '', notes: '' })

onMounted(async () => {
  if (isEdit.value) {
    await equipmentStore.fetchAll()
    const eq = equipmentStore.items.find((e) => e.id === Number(route.params.id))
    if (eq) {
      form.value = { name: eq.name, category: eq.category, notes: eq.notes || '' }
    }
  }
})

async function handleSubmit() {
  errorMsg.value = ''
  loading.value = true
  try {
    if (isEdit.value) {
      await equipmentStore.update(Number(route.params.id), form.value)
    } else {
      await equipmentStore.create(form.value)
    }
    router.push('/equipment')
  } catch (e) {
    errorMsg.value = e.response?.data?.detail || '保存に失敗しました'
  } finally {
    loading.value = false
  }
}
</script>
