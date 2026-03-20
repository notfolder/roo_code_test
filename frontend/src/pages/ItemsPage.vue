<template>
  <v-app>
    <v-main>
      <v-container>
        <div class="d-flex justify-space-between align-center mb-4">
          <div class="text-h6">備品一覧</div>
          <v-btn color="primary" @click="fetchItems">再読込</v-btn>
        </div>
        <v-simple-table>
          <thead>
            <tr>
              <th>コード</th>
              <th>名称</th>
              <th>状態</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in items" :key="item.id">
              <td>{{ item.item_code }}</td>
              <td>{{ item.name }}</td>
              <td>{{ item.status }}</td>
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

const items = ref([])
const fetchItems = async () => {
  const res = await api.get('/items')
  items.value = res.data
}
onMounted(fetchItems)
</script>

<style scoped>
</style>
