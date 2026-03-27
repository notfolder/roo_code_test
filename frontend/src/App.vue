<template>
  <v-app>
    <v-app-bar density="compact" color="primary" dark>
      <v-toolbar-title>備品管理・貸出予約</v-toolbar-title>
      <v-spacer />
      <v-btn variant="text" to="/equipments" router>備品一覧</v-btn>
      <v-btn variant="text" to="/reservations" router>予約</v-btn>
      <v-btn variant="text" to="/lend-return" router>貸出/返却</v-btn>
      <v-btn variant="text" to="/admin" router>管理</v-btn>
      <v-btn variant="text" @click="logout">ログアウト</v-btn>
    </v-app-bar>
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const logout = () => {
  localStorage.removeItem('token')
  router.push('/login')
}
</script>
