<template>
  <!-- 備品一覧画面：全ユーザーが閲覧可能。一般社員は貸出可能備品のみ表示される -->
  <v-container>
    <h2 class="mb-4">貸出可能な備品一覧</h2>
    <EquipmentTable
      :items="equipmentStore.items"
      :loading="equipmentStore.loading"
      :show-status="authStore.isAdmin"
    />
  </v-container>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useEquipmentStore } from '../stores/equipment'
import EquipmentTable from '../components/EquipmentTable.vue'

const authStore = useAuthStore()
const equipmentStore = useEquipmentStore()

onMounted(() => {
  // 一般社員は貸出可能備品のみ取得する（管理担当者は全件取得）
  equipmentStore.fetchAll(!authStore.isAdmin)
})
</script>
