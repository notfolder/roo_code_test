<template>
  <v-app-bar color="primary" flat>
    <v-app-bar-title>備品管理システム</v-app-bar-title>
    <v-spacer />
    <template v-if="authStore.isAdmin">
      <v-btn text @click="router.push('/lend')" data-testid="lend-button">貸出</v-btn>
      <v-btn text @click="router.push('/return')" data-testid="return-button">返却</v-btn>
      <v-btn text @click="router.push('/items/manage')" data-testid="item-manage-button">備品管理</v-btn>
      <v-btn text @click="router.push('/users')" data-testid="user-manage-button">アカウント管理</v-btn>
    </template>
    <v-btn text @click="router.push('/history')" data-testid="history-button">履歴</v-btn>
    <v-btn text @click="authStore.logout()" data-testid="logout-button">ログアウト</v-btn>
  </v-app-bar>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
</script>
