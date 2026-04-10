<template>
  <v-dialog v-model="dialog" max-width="500">
    <v-card>
      <v-card-title>{{ editItem ? '備品編集' : '備品追加' }}</v-card-title>
      <v-card-text>
        <v-text-field
          v-model="form.id"
          label="管理番号"
          :disabled="!!editItem"
          data-testid="item-id"
        />
        <v-text-field
          v-model="form.name"
          label="備品名"
          data-testid="item-name"
        />
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn text @click="emit('cancel')">キャンセル</v-btn>
        <v-btn color="primary" @click="handleSave" data-testid="item-save-button">保存</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  modelValue: Boolean,
  editItem: { type: Object, default: null },
})
const emit = defineEmits(['update:modelValue', 'save', 'cancel'])

const dialog = computed({
  get: () => props.modelValue,
  set: (v) => emit('update:modelValue', v),
})

const form = ref({ id: '', name: '' })

watch(
  () => props.editItem,
  (item) => {
    if (item) {
      form.value = { id: item.id, name: item.name }
    } else {
      form.value = { id: '', name: '' }
    }
  },
  { immediate: true }
)

function handleSave() {
  emit('save', { ...form.value })
}
</script>
