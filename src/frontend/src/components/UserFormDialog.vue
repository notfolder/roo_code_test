<script setup>
import { computed, reactive, watch } from 'vue'

const props = defineProps({
  modelValue: Boolean,
  user: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['update:modelValue', 'save'])

const form = reactive({
  name: '',
  email: '',
  password: '',
  role: 'employee'
})

const isEdit = computed(() => Boolean(props.user))

watch(
  () => props.user,
  (user) => {
    if (user) {
      form.name = user.name
      form.email = user.email
      form.password = ''
      form.role = user.role
    } else {
      form.name = ''
      form.email = ''
      form.password = ''
      form.role = 'employee'
    }
  },
  { immediate: true }
)

const close = () => emit('update:modelValue', false)
const save = () => emit('save', { ...form })
</script>

<template>
  <v-dialog :model-value="modelValue" max-width="560" @update:model-value="emit('update:modelValue', $event)">
    <v-card>
      <v-card-title>{{ isEdit ? 'ユーザー編集' : 'ユーザー登録' }}</v-card-title>
      <v-card-text>
        <v-text-field v-model="form.name" label="氏名" variant="outlined" data-testid="user-name" />
        <v-text-field v-model="form.email" label="メール" type="email" variant="outlined" data-testid="user-email" />
        <v-text-field
          v-if="!isEdit"
          v-model="form.password"
          label="パスワード"
          type="password"
          variant="outlined"
          data-testid="user-password"
        />
        <v-select
          v-model="form.role"
          label="ロール"
          variant="outlined"
          :items="[
            { title: '総務', value: 'admin' },
            { title: '社員', value: 'employee' }
          ]"
          data-testid="user-role"
        />
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn variant="text" @click="close">キャンセル</v-btn>
        <v-btn color="primary" data-testid="user-save-button" @click="save">保存</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
