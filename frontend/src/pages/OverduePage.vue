<template>
  <v-app>
    <v-main>
      <v-container>
        <div class="d-flex justify-space-between align-center mb-4">
          <div class="text-h6">未返却一覧</div>
          <v-btn color="primary" @click="fetchList">再読込</v-btn>
        </div>
        <v-simple-table>
          <thead>
            <tr>
              <th>貸出ID</th>
              <th>予約ID</th>
              <th>開始</th>
              <th>返却予定</th>
              <th>実返却</th>
              <th>状態</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="l in loans" :key="l.id">
              <td>{{ l.id }}</td>
              <td>{{ l.reservation_id }}</td>
              <td>{{ l.loan_start_date }}</td>
              <td>{{ l.planned_return_date }}</td>
              <td>{{ l.actual_return_date }}</td>
              <td>{{ l.status }}</td>
            </tr>
          </tbody>
        </v-simple-table>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'

const loans = ref([])
const fetchList = async () => {
  const res = await api.get('/loans/overdue')
  loans.value = res.data
}

onMounted(fetchList)
</script>

<style scoped>
</style>
