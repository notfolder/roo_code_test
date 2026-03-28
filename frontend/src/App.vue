<template>
  <!-- アプリケーションルートコンポーネント -->
  <v-app>
    <!-- ログイン画面以外でヘッダーを表示する -->
    <AppHeader v-if="authStore.isLoggedIn" />
    <!-- ルーターのビュー切り替え領域 -->
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script setup>
import { useAuthStore } from './stores/auth'
import AppHeader from './components/AppHeader.vue'

const authStore = useAuthStore()
</script>
