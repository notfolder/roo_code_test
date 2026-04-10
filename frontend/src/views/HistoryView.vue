<template>
  <v-app>
    <v-app-bar color="primary" flat>
      <v-app-bar-title>貸出履歴</v-app-bar-title>
      <v-spacer />
      <v-btn text @click="router.push('/')" data-testid="back-button">戻る</v-btn>
    </v-app-bar>
    <v-main>
      <v-container>
        <v-table>
          <thead>
            <tr>
              <th>備品名</th>
              <th>管理番号</th>
              <th>借用者名</th>
              <th>貸出日</th>
              <th>返却日</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="record in lendingStore.lendingRecords" :key="record.id">
              <td>{{ record.item_name }}</td>
              <td>{{ record.item_id }}</td>
              <td>{{ record.borrower_name }}</td>
              <td>{{ record.lend_date }}</td>
              <td>{{ record.return_date || '' }}</td>
            </tr>
          </tbody>
        </v-table>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useLendingStore } from '@/stores/lending'

const router = useRouter()
const lendingStore = useLendingStore()

onMounted(() => lendingStore.fetchLendingRecords())
</script>
