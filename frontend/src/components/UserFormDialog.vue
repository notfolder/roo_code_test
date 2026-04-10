<template>
  <v-dialog v-model="dialog" max-width="500">
    <v-card>
      <v-card-title>アカウント追加</v-card-title>
      <v-card-text>
        <v-text-field v-model="form.login_id" label="ログインID" data-testid="user-login-id" />
        <v-text-field v-model="form.password" label="パスワード" type="password" data-testid="user-password" />
        <v-select
          v-model="form.role"
          :items="roleItems"
          item-title="label"
          item-value="value"
          label="ロール"
          data-testid="user-role"
        />
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn text @click="emit('cancel')">キャンセル</v-btn>
        <v-btn color="primary" @click="handleSave" data-testid="user-save-button">保存</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({ modelValue: Boolean })
const emit = defineEmits(['update:modelValue', 'save', 'cancel'])

const dialog = computed({
  get: () => props.modelValue,
  set: (v) => emit('update:modelValue', v),
})

const roleItems = [
  { label: '管理者', value: 'admin' },
  { label: '一般ユーザー', value: 'user' },
]

const form = ref({ login_id: '', password: '', role: 'user' })

function handleSave() {
  emit('save', { ...form.value })
  form.value = { login_id: '', password: '', role: 'user' }
}
</script>
