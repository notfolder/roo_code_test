<template>
  <!-- 返却ダイアログ：貸出中の備品の返却を確認して登録する -->
  <v-dialog v-model="dialog" max-width="400" persistent>
    <v-card>
      <v-card-title>返却確認</v-card-title>
      <v-card-text>
        <p>
          <strong>{{ props.equipment?.management_number }} {{ props.equipment?.name }}</strong>
        </p>
        <p>借用者：{{ props.activeLoan?.borrower_name }}</p>
        <p class="mt-2">を返却しますか？</p>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn variant="text" @click="handleCancel">キャンセル</v-btn>
        <v-btn color="warning" :loading="loading" @click="handleSubmit">返却</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  /** ダイアログの表示状態 */
  modelValue: { type: Boolean, default: false },
  /** 返却対象の備品 */
  equipment: { type: Object, default: null },
  /** 対象の貸出記録 */
  activeLoan: { type: Object, default: null },
})

const emit = defineEmits(['update:modelValue', 'submitted'])

const loading = ref(false)

const dialog = computed({
  get: () => props.modelValue,
  set: (v) => emit('update:modelValue', v),
})

/** 返却を実行し、親コンポーネントにイベントを通知する */
async function handleSubmit() {
  loading.value = true
  try {
    emit('submitted', { loanId: props.activeLoan.id })
    dialog.value = false
  } finally {
    loading.value = false
  }
}

function handleCancel() {
  dialog.value = false
}
</script>
