<template>
  <v-container>
    <v-toolbar color="primary" dark flat class="mb-4 rounded">
      <v-btn icon @click="router.push('/')"><v-icon>mdi-arrow-left</v-icon></v-btn>
      <v-toolbar-title>備品マスタ管理</v-toolbar-title>
      <v-spacer />
      <v-btn color="white" variant="outlined" @click="openAddDialog" data-testid="btn-add-equipment">
        <v-icon left>mdi-plus</v-icon>新規追加
      </v-btn>
    </v-toolbar>

    <v-card>
      <v-data-table
        :headers="headers"
        :items="equipmentList"
        :loading="loading"
        no-data-text="備品が登録されていません"
        data-testid="equipment-management-table"
      >
        <template #item.status="{ item }">
          <v-chip :color="item.status === 'available' ? 'success' : 'warning'" size="small">
            {{ item.status === 'available' ? '利用可能' : '貸出中' }}
          </v-chip>
        </template>
        <template #item.actions="{ item }">
          <v-btn icon size="small" @click="openEditDialog(item)" data-testid="btn-edit">
            <v-icon>mdi-pencil</v-icon>
          </v-btn>
          <v-btn
            icon
            size="small"
            :disabled="item.status === 'lending'"
            @click="openDeleteDialog(item)"
            data-testid="btn-delete"
          >
            <v-icon>mdi-delete</v-icon>
          </v-btn>
        </template>
      </v-data-table>
    </v-card>

    <!-- 追加・編集ダイアログ -->
    <v-dialog v-model="formDialog" max-width="500" data-testid="equipment-form-dialog">
      <v-card>
        <v-card-title>{{ editTarget ? '備品編集' : '備品追加' }}</v-card-title>
        <v-card-text>
          <v-text-field
            v-model="form.management_number"
            label="管理番号"
            :rules="[v => !!v || '必須項目です']"
            data-testid="input-management-number"
          />
          <v-text-field
            v-model="form.name"
            label="備品名"
            :rules="[v => !!v || '必須項目です']"
            data-testid="input-name"
          />
          <v-text-field
            v-model="form.equipment_type"
            label="種別"
            :rules="[v => !!v || '必須項目です']"
            data-testid="input-equipment-type"
          />
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn text @click="formDialog = false">キャンセル</v-btn>
          <v-btn color="primary" @click="saveEquipment" data-testid="btn-save-equipment">保存</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- 削除確認ダイアログ -->
    <v-dialog v-model="deleteDialog" max-width="400" data-testid="delete-confirm-dialog">
      <v-card>
        <v-card-title>削除確認</v-card-title>
        <v-card-text>「{{ deleteTarget?.name }}」を削除しますか？この操作は元に戻せません。</v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn text @click="deleteDialog = false">キャンセル</v-btn>
          <v-btn color="error" @click="confirmDelete" data-testid="btn-confirm-delete">削除</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-snackbar v-model="snackbar" :color="snackbarColor" timeout="3000">
      {{ snackbarMessage }}
    </v-snackbar>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getEquipmentList, createEquipment, updateEquipment, deleteEquipment } from '../api/client.js'

const router = useRouter()

const equipmentList = ref([])
const loading = ref(false)
const formDialog = ref(false)
const deleteDialog = ref(false)
const editTarget = ref(null)
const deleteTarget = ref(null)
const snackbar = ref(false)
const snackbarMessage = ref('')
const snackbarColor = ref('success')

const form = ref({ management_number: '', name: '', equipment_type: '' })

const headers = [
  { title: '管理番号', key: 'management_number' },
  { title: '備品名', key: 'name' },
  { title: '種別', key: 'equipment_type' },
  { title: '状態', key: 'status' },
  { title: '操作', key: 'actions', sortable: false },
]

async function fetchEquipmentList() {
  loading.value = true
  try {
    const response = await getEquipmentList()
    equipmentList.value = response.data
  } catch {
    showSnackbar('備品一覧の取得に失敗しました', 'error')
  } finally {
    loading.value = false
  }
}

function openAddDialog() {
  editTarget.value = null
  form.value = { management_number: '', name: '', equipment_type: '' }
  formDialog.value = true
}

function openEditDialog(item) {
  editTarget.value = item
  form.value = { management_number: item.management_number, name: item.name, equipment_type: item.equipment_type }
  formDialog.value = true
}

function openDeleteDialog(item) {
  deleteTarget.value = item
  deleteDialog.value = true
}

async function saveEquipment() {
  try {
    if (editTarget.value) {
      await updateEquipment(editTarget.value.id, form.value)
      showSnackbar('備品を更新しました')
    } else {
      await createEquipment(form.value)
      showSnackbar('備品を追加しました')
    }
    formDialog.value = false
    await fetchEquipmentList()
  } catch (error) {
    showSnackbar(error.response?.data?.detail || '保存に失敗しました', 'error')
  }
}

async function confirmDelete() {
  try {
    await deleteEquipment(deleteTarget.value.id)
    showSnackbar('備品を削除しました')
    deleteDialog.value = false
    await fetchEquipmentList()
  } catch (error) {
    showSnackbar(error.response?.data?.detail || '削除に失敗しました', 'error')
  }
}

function showSnackbar(message, color = 'success') {
  snackbarMessage.value = message
  snackbarColor.value = color
  snackbar.value = true
}

onMounted(fetchEquipmentList)
</script>
