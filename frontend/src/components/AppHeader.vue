<template>
  <!-- 全画面共通ヘッダー：ナビゲーションメニューとログアウトボタンを表示する -->
  <v-app-bar color="primary" elevation="2">
    <v-app-bar-title>社内備品管理・貸出管理システム</v-app-bar-title>

    <template v-slot:append>
      <!-- 管理担当者のみナビゲーションメニューを表示する -->
      <template v-if="authStore.isAdmin">
        <v-btn :to="'/loans'" variant="text">貸出管理</v-btn>
        <v-btn :to="'/equipment'" variant="text">備品管理</v-btn>
        <v-btn :to="'/accounts'" variant="text">アカウント管理</v-btn>
      </template>
      <v-btn icon @click="handleLogout">
        <v-icon>mdi-logout</v-icon>
        <v-tooltip activator="parent">ログアウト</v-tooltip>
      </v-btn>
    </template>
  </v-app-bar>
</template>

<script setup>
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

/** ログアウトしてログイン画面に遷移する */
async function handleLogout() {
  await authStore.logout()
  router.push('/login')
}
</script>
