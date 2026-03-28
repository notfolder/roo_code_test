<template>
  <!-- 備品管理画面（管理担当者専用） -->
  <v-container>
    <div class="d-flex align-center mb-4">
      <h2>備品管理</h2>
      <v-spacer />
      <v-btn color="primary" prepend-icon="mdi-plus" @click="openCreateDialog">
        備品登録
      </v-btn>
    </div>

    <!-- エラーメッセージ -->
    <v-alert v-if="errorMessage" type="error" class="mb-4" density="compact" closable @click:close="errorMessage = ''">
      {{ errorMessage }}
    </v-alert>

    <!-- 備品一覧テーブル（編集・削除ボタン付き） -->
    <EquipmentTable
      :items="equipmentStore.items"
      :loading="equipmentStore.loading"
      :show-status="true"
      :show-manage-actions="true"
      @edit-click="openEditDialog"
      @delete-click="openDeleteDialog"
    />

    <!-- 備品登録・編集ダイアログ -->
    <EquipmentFormDialog
      v-model="formDialogOpen"
      :equipment="selectedEquipment"
      @submitted="handleFormSubmit"
    />

    <!-- 削除確認ダイアログ -->
    <v-dialog v-model="deleteDialogOpen" max-width="400">
      <v-card>
        <v-card-title>削除確認</v-card-title>
        <v-card-text>
          <p>
            <strong>{{ selectedEquipment?.management_number }} {{ selectedEquipment?.name }}</strong>
          </p>
          <p>を削除してもよいですか？</p>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="deleteDialogOpen = false">キャンセル</v-btn>
          <v-btn color="error" :loading="deleteLoading" @click="handleDelete">削除</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useEquipmentStore } from '../stores/equipment'
import EquipmentTable from '../components/EquipmentTable.vue'
import EquipmentFormDialog from '../components/EquipmentFormDialog.vue'

const equipmentStore = useEquipmentStore()

const formDialogOpen = ref(false)
const deleteDialogOpen = ref(false)
const selectedEquipment = ref(null)
const deleteLoading = ref(false)
const errorMessage = ref('')

onMounted(() => {
  equipmentStore.fetchAll(false)
})

/** 備品登録ダイアログを開く（登録モード） */
function openCreateDialog() {
  selectedEquipment.value = null
  formDialogOpen.value = true
}

/** 備品編集ダイアログを開く（編集モード） */
function openEditDialog(equipment) {
  selectedEquipment.value = equipment
  formDialogOpen.value = true
}

/** 削除確認ダイアログを開く */
function openDeleteDialog(equipment) {
  selectedEquipment.value = equipment
  deleteDialogOpen.value = true
}

/** 備品の登録または更新を実行する */
async function handleFormSubmit({ id, data }) {
  try {
    if (id) {
      await equipmentStore.update(id, data)
    } else {
      await equipmentStore.create(data)
    }
  } catch (error) {
    errorMessage.value = error.response?.data?.detail ?? '操作に失敗しました'
  }
}

/** 備品を削除する */
async function handleDelete() {
  deleteLoading.value = true
  try {
    await equipmentStore.remove(selectedEquipment.value.id)
    deleteDialogOpen.value = false
  } catch (error) {
    errorMessage.value = error.response?.data?.detail ?? '削除に失敗しました'
    deleteDialogOpen.value = false
  } finally {
    deleteLoading.value = false
  }
}
</script>
