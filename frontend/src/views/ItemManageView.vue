<template>
  <v-app>
    <v-app-bar color="primary" flat>
      <v-app-bar-title>備品管理</v-app-bar-title>
      <v-spacer />
      <v-btn text @click="router.push('/')" data-testid="back-button">戻る</v-btn>
    </v-app-bar>
    <v-main>
      <v-container>
        <v-snackbar v-model="snackbar" :color="snackbarColor" timeout="4000">{{ snackbarMessage }}</v-snackbar>
        <div class="d-flex justify-end mb-4">
          <v-btn color="primary" @click="openAdd" data-testid="item-add-button">+ 備品追加</v-btn>
        </div>
        <v-table>
          <thead>
            <tr>
              <th>管理番号</th>
              <th>備品名</th>
              <th>状態</th>
              <th>編集</th>
              <th>削除</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in itemStore.items" :key="item.id">
              <td>{{ item.id }}</td>
              <td>{{ item.name }}</td>
              <td>{{ item.status === 'available' ? '利用可能' : '貸出中' }}</td>
              <td>
                <v-btn size="small" @click="openEdit(item)" :data-testid="`item-edit-button-${item.id}`">編集</v-btn>
              </td>
              <td>
                <v-btn size="small" color="error" @click="confirmDelete(item)" :data-testid="`item-delete-button-${item.id}`">削除</v-btn>
              </td>
            </tr>
          </tbody>
        </v-table>
      </v-container>
    </v-main>

    <ItemFormDialog
      v-model="formDialog"
      :edit-item="editTarget"
      @save="handleSave"
      @cancel="formDialog = false"
    />
    <ConfirmDialog
      v-model="confirmDialogVisible"
      title="備品削除"
      message="この備品を削除しますか？"
      @confirm="handleDelete"
      @cancel="confirmDialogVisible = false"
    />
  </v-app>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useItemStore } from '@/stores/item'
import ItemFormDialog from '@/components/ItemFormDialog.vue'
import ConfirmDialog from '@/components/ConfirmDialog.vue'

const router = useRouter()
const itemStore = useItemStore()
const formDialog = ref(false)
const editTarget = ref(null)
const confirmDialogVisible = ref(false)
const deleteTarget = ref(null)
const snackbar = ref(false)
const snackbarMessage = ref('')
const snackbarColor = ref('error')

onMounted(() => itemStore.fetchItems())

function openAdd() {
  editTarget.value = null
  formDialog.value = true
}

function openEdit(item) {
  editTarget.value = item
  formDialog.value = true
}

async function handleSave(data) {
  try {
    if (editTarget.value) {
      await itemStore.updateItem(editTarget.value.id, { name: data.name })
    } else {
      await itemStore.createItem(data)
    }
    formDialog.value = false
    await itemStore.fetchItems()
    snackbarColor.value = 'success'
    snackbarMessage.value = '保存しました'
    snackbar.value = true
  } catch (e) {
    snackbarColor.value = 'error'
    snackbarMessage.value = e.response?.data?.detail || '保存に失敗しました'
    snackbar.value = true
  }
}

function confirmDelete(item) {
  deleteTarget.value = item
  confirmDialogVisible.value = true
}

async function handleDelete() {
  confirmDialogVisible.value = false
  try {
    await itemStore.deleteItem(deleteTarget.value.id)
    await itemStore.fetchItems()
    snackbarColor.value = 'success'
    snackbarMessage.value = '削除しました'
    snackbar.value = true
  } catch (e) {
    snackbarColor.value = 'error'
    snackbarMessage.value = e.response?.data?.detail || '削除に失敗しました'
    snackbar.value = true
  }
}
</script>
