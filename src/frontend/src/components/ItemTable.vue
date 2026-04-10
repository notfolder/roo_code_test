<script setup>
defineProps({
  items: {
    type: Array,
    required: true
  },
  isAdmin: {
    type: Boolean,
    required: true
  }
})

const emit = defineEmits(['loan', 'return', 'edit'])
</script>

<template>
  <v-table class="bg-white rounded">
    <thead>
      <tr>
        <th>資産番号</th>
        <th>名称</th>
        <th>状態</th>
        <th>貸出先</th>
        <th v-if="isAdmin">操作</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="item in items" :key="item.id" :data-testid="`item-row-${item.asset_number}`">
        <td>{{ item.asset_number }}</td>
        <td>{{ item.name }}</td>
        <td>
          <v-chip :color="item.state === 'available' ? 'teal' : 'orange'" size="small" text-color="white">
            {{ item.state === 'available' ? '貸出可' : '貸出中' }}
          </v-chip>
        </td>
        <td>{{ item.current_user_name || '---' }}</td>
        <td v-if="isAdmin">
          <v-btn
            v-if="item.state === 'available'"
            size="small"
            color="secondary"
            variant="tonal"
            class="mr-2"
            :data-testid="`loan-button-${item.asset_number}`"
            @click="emit('loan', item)"
          >
            貸出
          </v-btn>
          <v-btn
            v-if="item.state === 'lent'"
            size="small"
            color="accent"
            variant="tonal"
            class="mr-2"
            :data-testid="`return-button-${item.asset_number}`"
            @click="emit('return', item)"
          >
            返却
          </v-btn>
          <v-btn
            size="small"
            color="primary"
            variant="text"
            :data-testid="`edit-item-button-${item.asset_number}`"
            @click="emit('edit', item)"
          >
            編集
          </v-btn>
        </td>
      </tr>
    </tbody>
  </v-table>
</template>
