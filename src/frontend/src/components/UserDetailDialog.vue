<script setup>
defineProps({
  modelValue: Boolean,
  user: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['update:modelValue'])
</script>

<template>
  <v-dialog :model-value="modelValue" max-width="500" @update:model-value="emit('update:modelValue', $event)">
    <v-card>
      <v-card-title>ユーザー詳細</v-card-title>
      <v-card-text>
        <div class="mb-2">氏名: {{ user?.name }}</div>
        <div class="mb-2">メール: {{ user?.email }}</div>
        <div class="mb-2">権限: {{ user?.role === 'admin' ? '総務' : '社員' }}</div>
        <div>ステータス: {{ user?.status === 'active' ? '有効' : '削除済' }}</div>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn color="primary" @click="emit('update:modelValue', false)">閉じる</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
