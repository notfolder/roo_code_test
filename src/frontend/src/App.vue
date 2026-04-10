<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from './stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const isLoggedIn = computed(() => authStore.isAuthenticated)
const isAdmin = computed(() => authStore.isAdmin)

const logout = () => {
  authStore.clearSession()
  router.push({ name: 'login' })
}
</script>

<template>
  <v-app>
    <v-app-bar color="primary" density="comfortable" elevation="2">
      <v-app-bar-title>備品管理・貸出管理アプリ</v-app-bar-title>
      <v-spacer />
      <template v-if="isLoggedIn">
        <v-btn variant="text" :to="{ name: 'items' }">備品一覧</v-btn>
        <v-btn v-if="isAdmin" variant="text" :to="{ name: 'users' }">ユーザー管理</v-btn>
        <v-btn variant="outlined" color="accent" data-testid="logout-button" @click="logout">ログアウト</v-btn>
      </template>
    </v-app-bar>

    <v-main>
      <v-container class="py-8">
        <router-view :key="route.fullPath" />
      </v-container>
    </v-main>
  </v-app>
</template>
