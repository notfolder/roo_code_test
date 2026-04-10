<template>
  <v-app>
    <AppBar />
    <v-main>
      <v-container>
        <h2 class="mb-4">貸出登録</h2>
        <v-snackbar v-model="snackbar" :color="snackbarColor" timeout="4000">{{ snackbarMessage }}</v-snackbar>
        <v-select
          v-model="form.item_id"
          :items="availableItems"
          item-title="label"
          item-value="value"
          label="備品"
          data-testid="lend-item"
        />
        <v-select
          v-model="form.borrower_user_id"
          :items="userItems"
          item-title="label"
          item-value="value"
          label="借用者"
          data-testid="lend-borrower"
        />
        <v-text-field
          v-model="form.lend_date"
          label="貸出日"
          type="date"
          data-testid="lend-date"
        />
        <v-btn color="primary" @click="handleSubmit" data-testid="lend-submit-button">登録</v-btn>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import AppBar from '@/components/AppBar.vue'
import { useItemStore } from '@/stores/item'
import { useUserStore } from '@/stores/user'
import { useLendingStore } from '@/stores/lending'

const router = useRouter()
const itemStore = useItemStore()
const userStore = useUserStore()
const lendingStore = useLendingStore()

const today = new Date().toISOString().slice(0, 10)
const form = ref({ item_id: '', borrower_user_id: null, lend_date: today })
const snackbar = ref(false)
const snackbarMessage = ref('')
const snackbarColor = ref('error')

const availableItems = computed(() =>
  itemStore.items
    .filter((i) => i.status === 'available')
    .map((i) => ({ label: `${i.id}: ${i.name}`, value: i.id }))
)
const userItems = computed(() =>
  userStore.users.map((u) => ({ label: u.login_id, value: u.id }))
)

onMounted(async () => {
  await Promise.all([itemStore.fetchItems(), userStore.fetchUsers()])
})

async function handleSubmit() {
  try {
    await lendingStore.createLendingRecord({
      item_id: form.value.item_id,
      borrower_user_id: form.value.borrower_user_id,
      lend_date: form.value.lend_date,
    })
    await itemStore.fetchItems()
    router.push('/')
  } catch (e) {
    snackbarColor.value = 'error'
    snackbarMessage.value = e.response?.data?.detail || '登録に失敗しました'
    snackbar.value = true
  }
}
</script>
