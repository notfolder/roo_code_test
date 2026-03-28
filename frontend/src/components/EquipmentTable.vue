<template>
  <!--
    備品テーブルコンポーネント
    備品一覧画面・貸出管理画面・備品管理画面の3箇所で共用する
    propsで表示内容と操作ボタンを切り替える
  -->
  <v-data-table
    :headers="headers"
    :items="props.items"
    :loading="props.loading"
    no-data-text="備品がありません"
    loading-text="読み込み中..."
    items-per-page="20"
  >
    <!-- 状態列のカスタム表示 -->
    <template v-slot:item.status="{ item }" v-if="props.showStatus">
      <v-chip :color="item.status === 'available' ? 'success' : 'warning'" size="small">
        {{ item.status === 'available' ? '貸出可' : '貸出中' }}
      </v-chip>
    </template>

    <!-- 操作列：貸出管理画面用（貸出・返却ボタン） -->
    <template v-slot:item.loan_action="{ item }" v-if="props.showLoanActions">
      <v-btn
        v-if="item.status === 'available'"
        color="primary"
        size="small"
        variant="outlined"
        @click="emit('loanClick', item)"
      >
        貸出
      </v-btn>
      <v-btn
        v-else
        color="warning"
        size="small"
        variant="outlined"
        @click="emit('returnClick', item)"
      >
        返却
      </v-btn>
    </template>

    <!-- 操作列：備品管理画面用（編集・削除ボタン） -->
    <template v-slot:item.manage_action="{ item }" v-if="props.showManageActions">
      <v-btn
        color="primary"
        size="small"
        variant="text"
        icon="mdi-pencil"
        @click="emit('editClick', item)"
      />
      <v-btn
        color="error"
        size="small"
        variant="text"
        icon="mdi-delete"
        @click="emit('deleteClick', item)"
      />
    </template>

    <!-- 貸出管理画面：借用者列 -->
    <template v-slot:item.borrower_name="{ item }" v-if="props.showBorrower">
      {{ activeLoanMap[item.id]?.borrower_name ?? '' }}
    </template>
  </v-data-table>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  /** 表示する備品一覧 */
  items: { type: Array, default: () => [] },
  /** ローディング中かどうか */
  loading: { type: Boolean, default: false },
  /** 状態列（貸出可/貸出中）を表示するか */
  showStatus: { type: Boolean, default: false },
  /** 貸出・返却ボタンを表示するか */
  showLoanActions: { type: Boolean, default: false },
  /** 編集・削除ボタンを表示するか */
  showManageActions: { type: Boolean, default: false },
  /** 借用者列を表示するか */
  showBorrower: { type: Boolean, default: false },
  /** 貸出中備品のloan情報マップ（equipment_id → LoanRecord） */
  activeLoanMap: { type: Object, default: () => ({}) },
})

const emit = defineEmits(['loanClick', 'returnClick', 'editClick', 'deleteClick'])

/** propsに応じてヘッダーを動的に生成する */
const headers = computed(() => {
  const base = [
    { title: '管理番号', key: 'management_number', sortable: true },
    { title: '備品名', key: 'name', sortable: true },
  ]
  if (props.showStatus) {
    base.push({ title: '状態', key: 'status', sortable: true })
  }
  if (props.showBorrower) {
    base.push({ title: '借用者', key: 'borrower_name', sortable: false })
  }
  base.push({ title: '備考', key: 'note', sortable: false })
  if (props.showLoanActions) {
    base.push({ title: '操作', key: 'loan_action', sortable: false, align: 'center' })
  }
  if (props.showManageActions) {
    base.push({ title: '操作', key: 'manage_action', sortable: false, align: 'center' })
  }
  return base
})
</script>
