<template>
  <v-container max-width="600">
    <v-toolbar color="primary" dark flat class="mb-4 rounded">
      <v-btn icon @click="router.push('/')"><v-icon>mdi-arrow-left</v-icon></v-btn>
      <v-toolbar-title>貸出記録登録</v-toolbar-title>
    </v-toolbar>

    <v-card>
      <v-card-text>
        <v-select
          v-model="form.equipment_id"
          :items="availableEquipment"
          item-title="label"
          item-value="id"
          label="備品を選択"
          :rules="[v => !!v || '備品を選択してください']"
          data-testid="select-equipment"
        />
        <v-text-field
          v-model="form.borrower_name"
          label="借用者名"
          :rules="[v => !!v || '借用者名を入力してください']"
          data-testid="input-borrower-name"
        />
        <v-text-field
          v-model="form.lent_at"
          label="貸出日"
          type="date"
          :rules="[v => !!v || '貸出日を入力してください']"
          data-testid="input-lent-at"
        />
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn text @click="router.push('/')">キャンセル</v-btn>
        <v-btn color="primary" @click="handleSubmit" data-testid="btn-save-lending">保存</v-btn>
      </v-card-actions>
    </v-card>

    <v-snackbar v-model="snackbar" :color="snackbarColor" timeout="3000">
      {{ snackbarMessage }}
    </v-snackbar>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getEquipmentList, createLending } from '../api/client.js'

const router = useRouter()

const availableEquipment = ref([])
const snackbar = ref(false)
const snackbarMessage = ref('')
const snackbarColor = ref('success')

const today = new Date().toISOString().slice(0, 10)
const form = ref({ equipment_id: null, borrower_name: '', lent_at: today })

async function fetchAvailableEquipment() {
  try {
    const response = await getEquipmentList()
    availableEquipment.value = response.data
      .filter(e => e.status === 'available')
      .map(e => ({ id: e.id, label: `${e.management_number} ${e.name}` }))
  } catch {
    showSnackbar('備品一覧の取得に失敗しました', 'error')
  }
}

async function handleSubmit() {
  if (!form.value.equipment_id || !form.value.borrower_name || !form.value.lent_at) {
    showSnackbar('すべての項目を入力してください', 'error')
    return
  }
  try {
    await createLending(form.value)
    showSnackbar('貸出記録を登録しました')
    setTimeout(() => router.push('/'), 1000)
  } catch (error) {
    showSnackbar(error.response?.data?.detail || '登録に失敗しました', 'error')
  }
}

function showSnackbar(message, color = 'success') {
  snackbarMessage.value = message
  snackbarColor.value = color
  snackbar.value = true
}

onMounted(fetchAvailableEquipment)
</script>
