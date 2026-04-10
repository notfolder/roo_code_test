<template>
  <v-dialog v-model="dialog" max-width="400">
    <v-card>
      <v-card-title>{{ title }}</v-card-title>
      <v-card-text>{{ message }}</v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn text @click="emit('cancel')">キャンセル</v-btn>
        <v-btn color="error" @click="emit('confirm')" data-testid="confirm-button">削除</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: Boolean,
  title: String,
  message: String,
})
const emit = defineEmits(['update:modelValue', 'confirm', 'cancel'])

const dialog = computed({
  get: () => props.modelValue,
  set: (v) => emit('update:modelValue', v),
})
</script>
