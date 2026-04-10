<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  modelValue: Boolean,
  item: {
    type: Object,
    default: null
  },
  users: {
    type: Array,
    required: true
  }
})

const emit = defineEmits(['update:modelValue', 'confirm'])
const selectedUser = ref('')

watch(
  () => props.modelValue,
  (opened) => {
    if (opened) {
      selectedUser.value = props.users[0]?.id || ''
    }
  }
)

const close = () => emit('update:modelValue', false)
const confirm = () => {
  emit('confirm', selectedUser.value)
}
</script>

<template>
  <v-dialog :model-value="modelValue" max-width="560" @update:model-value="emit('update:modelValue', $event)">
    <v-card>
      <v-card-title>貸出処理</v-card-title>
      <v-card-text>
        <div class="mb-4" data-testid="loan-item-label">備品: {{ item?.asset_number }} {{ item?.name }}</div>
        <v-select
          v-model="selectedUser"
          label="貸出先社員"
          variant="outlined"
          item-title="name"
          item-value="id"
          :items="users"
          data-testid="loan-user-select"
        />
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn variant="text" @click="close">キャンセル</v-btn>
        <v-btn color="secondary" data-testid="loan-confirm-button" @click="confirm">貸出を確定</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
