<script setup>
const props = defineProps({
  modelValue: Boolean,
  item: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['update:modelValue', 'confirm'])

const close = () => emit('update:modelValue', false)
</script>

<template>
  <v-dialog :model-value="modelValue" max-width="520" @update:model-value="emit('update:modelValue', $event)">
    <v-card>
      <v-card-title>返却処理</v-card-title>
      <v-card-text>
        <div class="mb-2">備品: {{ item?.asset_number }} {{ item?.name }}</div>
        <div class="mb-2">貸出先: {{ item?.current_user_name || '---' }}</div>
        <div>返却日時: 自動設定</div>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn variant="text" @click="close">キャンセル</v-btn>
        <v-btn color="accent" data-testid="return-confirm-button" @click="emit('confirm')">返却を確定</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
