<script setup>
import { computed, reactive, watch } from 'vue'

const props = defineProps({
  modelValue: Boolean,
  item: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['update:modelValue', 'save'])

const form = reactive({
  asset_number: '',
  name: '',
  state: 'available'
})

const isEdit = computed(() => Boolean(props.item))

watch(
  () => props.item,
  (item) => {
    if (item) {
      form.asset_number = item.asset_number
      form.name = item.name
      form.state = item.state
    } else {
      form.asset_number = ''
      form.name = ''
      form.state = 'available'
    }
  },
  { immediate: true }
)

const close = () => emit('update:modelValue', false)
const save = () => {
  emit('save', { ...form })
}
</script>

<template>
  <v-dialog :model-value="modelValue" max-width="560" @update:model-value="emit('update:modelValue', $event)">
    <v-card>
      <v-card-title>{{ isEdit ? '備品編集' : '備品登録' }}</v-card-title>
      <v-card-text>
        <v-text-field
          v-model="form.asset_number"
          :disabled="isEdit"
          label="資産管理番号"
          variant="outlined"
          data-testid="item-asset-number"
        />
        <v-text-field v-model="form.name" label="名称" variant="outlined" data-testid="item-name" />
        <v-select
          v-model="form.state"
          label="状態"
          variant="outlined"
          :items="[
            { title: '貸出可', value: 'available' },
            { title: '貸出中', value: 'lent' }
          ]"
          data-testid="item-state"
        />
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn variant="text" @click="close">キャンセル</v-btn>
        <v-btn color="primary" data-testid="item-save-button" @click="save">保存</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
