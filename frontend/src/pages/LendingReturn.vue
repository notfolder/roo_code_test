<template>
  <v-container max-width="600">
    <v-toolbar color="primary" dark flat class="mb-4 rounded">
      <v-btn icon @click="router.push('/')"><v-icon>mdi-arrow-left</v-icon></v-btn>
      <v-toolbar-title>返却記録登録</v-toolbar-title>
    </v-toolbar>

    <v-card>
      <v-card-text>
        <v-select
          v-model="selectedLendingId"
          :items="activeLendings"
          item-title="label"
          item-value="id"
          label="返却する貸出記録を選択"
          :rules="[v => !!v || '貸出記録を選択してください']"
          data-testid="select-lending"
        />
        <v-text-field
          v-model="returnedAt"
          label="返却日"
          type="date"
          :rules="[v => !!v || '返却日を入力してください']"
          data-testid="input-returned-at"
        />
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn text @click="router.push('/')">キャンセル</v-btn>
        <v-btn color="primary" @click="handleSubmit" data-testid="btn-save-return">保存</v-btn>
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
import { getActiveLending, returnLending } from '../api/client.js'

const router = useRouter()

const activeLendings = ref([])
const selectedLendingId = ref(null)
const snackbar = ref(false)
const snackbarMessage = ref('')
const snackbarColor = ref('success')

const today = new Date().toISOString().slice(0, 10)
const returnedAt = ref(today)

async function fetchActiveLendings() {
  try {
    const response = await getActiveLending()
    activeLendings.value = response.data.map(l => ({
      id: l.id,
      label: `${l.management_number} ${l.equipment_name} / ${l.borrower_name}`,
    }))
  } catch {
    showSnackbar('貸出中記録の取得に失敗しました', 'error')
  }
}

async function handleSubmit() {
  if (!selectedLendingId.value || !returnedAt.value) {
    showSnackbar('すべての項目を入力してください', 'error')
    return
  }
  try {
    await returnLending(selectedLendingId.value, returnedAt.value)
    showSnackbar('返却記録を登録しました')
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

onMounted(fetchActiveLendings)
</script>
