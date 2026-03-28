<template>
  <!-- 貸出ダイアログ：備品と借りる社員を選択して貸出を登録する -->
  <v-dialog v-model="dialog" max-width="480" persistent>
    <v-card>
      <v-card-title>貸出登録</v-card-title>
      <v-card-text>
        <p class="mb-4">
          備品: <strong>{{ props.equipment?.management_number }} {{ props.equipment?.name }}</strong>
        </p>
        <v-select
          v-model="selectedAccountId"
          :items="accountItems"
          item-title="label"
          item-value="id"
          label="借りる社員 *"
          :error-messages="accountError"
        />
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn variant="text" @click="handleCancel">キャンセル</v-btn>
        <v-btn color="primary" :loading="loading" @click="handleSubmit">貸出</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useAccountStore } from '../stores/account'

const props = defineProps({
  /** ダイアログの表示状態 */
  modelValue: { type: Boolean, default: false },
  /** 貸出対象の備品 */
  equipment: { type: Object, default: null },
})

const emit = defineEmits(['update:modelValue', 'submitted'])

const accountStore = useAccountStore()
const selectedAccountId = ref(null)
const accountError = ref('')
const loading = ref(false)

// v-modelのバインディング
const dialog = computed({
  get: () => props.modelValue,
  set: (v) => emit('update:modelValue', v),
})

// ダイアログを開いた時にアカウント一覧を取得し、入力をリセットする
watch(
  () => props.modelValue,
  async (val) => {
    if (val) {
      selectedAccountId.value = null
      accountError.value = ''
      await accountStore.fetchAll()
    }
  }
)

/** 一般社員のみ選択肢に表示する */
const accountItems = computed(() =>
  accountStore.items
    .filter((a) => a.role === 'employee')
    .map((a) => ({ id: a.id, label: a.account_name }))
)

/** 貸出登録を実行し、親コンポーネントにイベントを通知する */
async function handleSubmit() {
  if (!selectedAccountId.value) {
    accountError.value = '借りる社員を選択してください'
    return
  }
  accountError.value = ''
  loading.value = true
  try {
    emit('submitted', {
      equipmentId: props.equipment.id,
      borrowerAccountId: selectedAccountId.value,
    })
    dialog.value = false
  } finally {
    loading.value = false
  }
}

function handleCancel() {
  dialog.value = false
}
</script>
