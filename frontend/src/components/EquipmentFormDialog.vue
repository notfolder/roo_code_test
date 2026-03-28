<template>
  <!--
    備品登録・編集ダイアログ
    登録モード（equipment=null）と編集モード（equipment=オブジェクト）を1コンポーネントで処理する
  -->
  <v-dialog v-model="dialog" max-width="480" persistent>
    <v-card>
      <v-card-title>{{ isEditMode ? '備品編集' : '備品登録' }}</v-card-title>
      <v-card-text>
        <v-text-field
          v-model="form.management_number"
          label="管理番号 *"
          :error-messages="errors.management_number"
          @input="errors.management_number = ''"
        />
        <v-text-field
          v-model="form.name"
          label="備品名 *"
          :error-messages="errors.name"
          @input="errors.name = ''"
        />
        <v-text-field
          v-model="form.note"
          label="備考"
        />
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn variant="text" @click="handleCancel">キャンセル</v-btn>
        <v-btn color="primary" :loading="loading" @click="handleSubmit">
          {{ isEditMode ? '更新' : '登録' }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  /** ダイアログの表示状態 */
  modelValue: { type: Boolean, default: false },
  /** 編集対象の備品（nullの場合は登録モード） */
  equipment: { type: Object, default: null },
})

const emit = defineEmits(['update:modelValue', 'submitted'])

// 編集モードかどうか（備品が渡されている場合は編集モード）
const isEditMode = computed(() => props.equipment !== null)
const loading = ref(false)
const form = ref({ management_number: '', name: '', note: '' })
const errors = ref({ management_number: '', name: '' })

const dialog = computed({
  get: () => props.modelValue,
  set: (v) => emit('update:modelValue', v),
})

// ダイアログを開いた時にフォームを初期化する
watch(
  () => props.modelValue,
  (val) => {
    if (val) {
      // 編集モードの場合は既存値を初期表示する
      form.value = {
        management_number: props.equipment?.management_number ?? '',
        name: props.equipment?.name ?? '',
        note: props.equipment?.note ?? '',
      }
      errors.value = { management_number: '', name: '' }
    }
  }
)

/** バリデーションを実行する */
function validate() {
  let valid = true
  if (!form.value.management_number.trim()) {
    errors.value.management_number = '管理番号を入力してください'
    valid = false
  }
  if (!form.value.name.trim()) {
    errors.value.name = '備品名を入力してください'
    valid = false
  }
  return valid
}

/** フォームを送信し、親コンポーネントにイベントを通知する */
async function handleSubmit() {
  if (!validate()) return
  loading.value = true
  try {
    emit('submitted', {
      id: props.equipment?.id,
      data: { ...form.value, note: form.value.note || null },
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
