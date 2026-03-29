<template>
  <AppLayout>
    <div class="d-flex align-center mb-4">
      <h1 class="text-h5">備品一覧</h1>
      <v-spacer />
      <v-btn v-if="auth.isAdmin" color="primary" to="/equipment/create" prepend-icon="mdi-plus">備品登録</v-btn>
    </div>
    <v-card>
      <v-data-table
        :headers="headers"
        :items="equipmentStore.items"
        :loading="equipmentStore.loading"
        no-data-text="備品が登録されていません"
      >
        <template #item.status="{ item }">
          <v-chip :color="item.status === 'available' ? 'success' : 'warning'" size="small">
            {{ item.status === 'available' ? '貸出可' : '貸出中' }}
          </v-chip>
        </template>
        <template v-if="auth.isAdmin" #item.actions="{ item }">
          <v-btn icon size="small" variant="text" :to="`/equipment/${item.id}/edit`">
            <v-icon>mdi-pencil</v-icon>
          </v-btn>
          <v-btn icon size="small" variant="text" color="error" @click="confirmDelete(item)">
            <v-icon>mdi-delete</v-icon>
          </v-btn>
        </template>
      </v-data-table>
    </v-card>

    <v-dialog v-model="deleteDialog" max-width="400">
      <v-card>
        <v-card-title>削除確認</v-card-title>
        <v-card-text>「{{ deleteTarget?.name }}」を削除しますか？</v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn @click="deleteDialog = false">キャンセル</v-btn>
          <v-btn color="error" :loading="deleting" @click="handleDelete">削除</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import AppLayout from './AppLayout.vue'
import { useEquipmentStore } from '../stores/equipment.js'
import { useAuthStore } from '../stores/auth.js'

const equipmentStore = useEquipmentStore()
const auth = useAuthStore()

const deleteDialog = ref(false)
const deleteTarget = ref(null)
const deleting = ref(false)

const headers = computed(() => {
  const base = [
    { title: '管理番号', key: 'management_number' },
    { title: '品名', key: 'name' },
    { title: '状態', key: 'status' },
  ]
  if (auth.isAdmin) base.push({ title: '操作', key: 'actions', sortable: false })
  return base
})

function confirmDelete(item) {
  deleteTarget.value = item
  deleteDialog.value = true
}

async function handleDelete() {
  deleting.value = true
  try {
    await equipmentStore.remove(deleteTarget.value.id)
    deleteDialog.value = false
  } catch (e) {
    alert(e.response?.data?.detail || '削除に失敗しました')
  } finally {
    deleting.value = false
  }
}

onMounted(() => equipmentStore.fetchAll())
</script>
