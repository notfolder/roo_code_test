<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import ItemFormDialog from '../components/ItemFormDialog.vue'
import ItemTable from '../components/ItemTable.vue'
import LoanDialog from '../components/LoanDialog.vue'
import ReturnDialog from '../components/ReturnDialog.vue'
import api from '../services/api'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
const router = useRouter()

const items = ref([])
const users = ref([])
const loading = ref(false)
const message = ref('')
const errorMessage = ref('')

const showItemDialog = ref(false)
const showLoanDialog = ref(false)
const showReturnDialog = ref(false)

const selectedItem = ref(null)

const isAdmin = computed(() => authStore.isAdmin)
const loanUsers = computed(() => users.value.filter((user) => user.role === 'employee' && user.status === 'active'))

const fetchItems = async () => {
  const { data } = await api.get('/items')
  items.value = data
}

const fetchUsers = async () => {
  if (!isAdmin.value) {
    users.value = []
    return
  }
  const { data } = await api.get('/users')
  users.value = data
}

const load = async () => {
  loading.value = true
  errorMessage.value = ''
  try {
    await Promise.all([fetchItems(), fetchUsers()])
  } catch (error) {
    if (error.response?.status === 401) {
      authStore.clearSession()
      router.push({ name: 'login' })
      return
    }
    errorMessage.value = 'データの取得に失敗しました'
  } finally {
    loading.value = false
  }
}

const openCreateItem = () => {
  selectedItem.value = null
  showItemDialog.value = true
}

const openEditItem = (item) => {
  selectedItem.value = item
  showItemDialog.value = true
}

const saveItem = async (payload) => {
  message.value = ''
  errorMessage.value = ''
  try {
    if (selectedItem.value) {
      await api.put(`/items/${selectedItem.value.id}`, {
        name: payload.name,
        state: payload.state
      })
      message.value = '備品を更新しました'
    } else {
      await api.post('/items', payload)
      message.value = '備品を登録しました'
    }
    showItemDialog.value = false
    await fetchItems()
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || '備品の保存に失敗しました'
  }
}

const openLoan = (item) => {
  selectedItem.value = item
  showLoanDialog.value = true
}

const confirmLoan = async (userId) => {
  try {
    await api.post(`/items/${selectedItem.value.id}/loan`, { user_id: userId })
    message.value = '貸出処理を完了しました'
    showLoanDialog.value = false
    await fetchItems()
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || '貸出処理に失敗しました'
  }
}

const openReturn = (item) => {
  selectedItem.value = item
  showReturnDialog.value = true
}

const confirmReturn = async () => {
  try {
    await api.post(`/items/${selectedItem.value.id}/return`)
    message.value = '返却処理を完了しました'
    showReturnDialog.value = false
    await fetchItems()
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || '返却処理に失敗しました'
  }
}

onMounted(load)
</script>

<template>
  <v-card elevation="3">
    <v-card-title class="d-flex align-center">
      <span class="text-h6">備品一覧</span>
      <v-spacer />
      <v-btn v-if="isAdmin" color="primary" data-testid="create-item-button" @click="openCreateItem">備品登録</v-btn>
    </v-card-title>
    <v-card-text>
      <v-alert v-if="message" type="success" variant="tonal" class="mb-4">{{ message }}</v-alert>
      <v-alert v-if="errorMessage" type="error" variant="tonal" class="mb-4">{{ errorMessage }}</v-alert>
      <v-progress-linear v-if="loading" indeterminate color="primary" class="mb-4" />
      <item-table :items="items" :is-admin="isAdmin" @edit="openEditItem" @loan="openLoan" @return="openReturn" />
    </v-card-text>
  </v-card>

  <item-form-dialog v-model="showItemDialog" :item="selectedItem" @save="saveItem" />
  <loan-dialog v-model="showLoanDialog" :item="selectedItem" :users="loanUsers" @confirm="confirmLoan" />
  <return-dialog v-model="showReturnDialog" :item="selectedItem" @confirm="confirmReturn" />
</template>
