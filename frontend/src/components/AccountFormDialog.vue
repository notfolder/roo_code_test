<template>
  <!-- アカウント作成ダイアログ -->
  <v-dialog v-model="dialog" max-width="480" persistent>
    <v-card>
      <v-card-title>アカウント作成</v-card-title>
      <v-card-text>
        <v-text-field
          v-model="form.account_name"
          label="アカウント名 *"
          :error-messages="errors.account_name"
          @input="errors.account_name = ''"
        />
        <v-text-field
          v-model="form.password"
          label="パスワード *"
          type="password"
          :error-messages="errors.password"
          @input="errors.password = ''"
        />
        <v-radio-group v-model="form.role" label="役割 *" inline>
          <v-radio label="管理担当者" value="admin" />
          <v-radio label="一般社員" value="employee" />
        </v-radio-group>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn variant="text" @click="handleCancel">キャンセル</v-btn>
        <v-btn color="primary" :loading="loading" @click="handleSubmit">作成</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  /** ダイアログの表示状態 */
  modelValue: { type: Boolean, default: false },
})

const emit = defineEmits(['update:modelValue', 'submitted'])

const loading = ref(false)
const form = ref({ account_name: '', password: '', role: 'employee' })
const errors = ref({ account_name: '', password: '' })

const dialog = computed({
  get: () => props.modelValue,
  set: (v) => emit('update:modelValue', v),
})

// ダイアログを開いた時にフォームをリセットする
watch(
  () => props.modelValue,
  (val) => {
    if (val) {
      form.value = { account_name: '', password: '', role: 'employee' }
      errors.value = { account_name: '', password: '' }
    }
  }
)

/** バリデーションを実行する */
function validate() {
  let valid = true
  if (!form.value.account_name.trim()) {
    errors.value.account_name = 'アカウント名を入力してください'
    valid = false
  }
  if (form.value.password.length < 8) {
    errors.value.password = 'パスワードは8文字以上で入力してください'
    valid = false
  }
  return valid
}

/** フォームを送信し、親コンポーネントにイベントを通知する */
async function handleSubmit() {
  if (!validate()) return
  loading.value = true
  try {
    emit('submitted', { ...form.value })
    dialog.value = false
  } finally {
    loading.value = false
  }
}

function handleCancel() {
  dialog.value = false
}
</script>
