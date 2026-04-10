<template>
  <v-app>
    <AppBar />
    <v-main>
      <v-container>
        <h2 class="mb-4">備品一覧</h2>
        <v-snackbar v-model="snackbar" color="error" timeout="4000">{{ snackbarMessage }}</v-snackbar>
        <v-table>
          <thead>
            <tr>
              <th>管理番号</th>
              <th>備品名</th>
              <th>状態</th>
              <th>借用者</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in itemStore.items" :key="item.id" :data-testid="`item-row-${item.id}`">
              <td>{{ item.id }}</td>
              <td>{{ item.name }}</td>
              <td>{{ item.status === 'available' ? '利用可能' : '貸出中' }}</td>
              <td>{{ item.borrower_name || '' }}</td>
            </tr>
          </tbody>
        </v-table>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import AppBar from '@/components/AppBar.vue'
import { useItemStore } from '@/stores/item'

const itemStore = useItemStore()
const snackbar = ref(false)
const snackbarMessage = ref('')

onMounted(async () => {
  try {
    await itemStore.fetchItems()
  } catch (e) {
    snackbarMessage.value = 'データの取得に失敗しました'
    snackbar.value = true
  }
})
</script>
