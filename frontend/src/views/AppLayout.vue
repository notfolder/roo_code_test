<template>
  <v-navigation-drawer v-model="drawer">
    <v-list-item title="備品管理システム" nav />
    <v-divider />
    <v-list density="compact" nav>
      <v-list-item prepend-icon="mdi-view-dashboard" title="ダッシュボード" to="/" />
      <template v-if="auth.isAdmin">
        <v-list-item prepend-icon="mdi-package-variant-closed" title="備品管理" to="/equipment" />
        <v-list-item prepend-icon="mdi-plus-circle" title="貸出登録" to="/loans/create" />
        <v-list-item prepend-icon="mdi-keyboard-return" title="返却登録" to="/loans/return" />
        <v-list-item prepend-icon="mdi-account-multiple" title="ユーザー管理" to="/users" />
      </template>
    </v-list>
  </v-navigation-drawer>

  <v-app-bar>
    <v-app-bar-nav-icon @click="drawer = !drawer" />
    <v-toolbar-title>備品管理システム</v-toolbar-title>
    <v-spacer />
    <span class="mr-2 text-body-2">{{ auth.user?.name }}</span>
    <v-btn variant="outlined" size="small" prepend-icon="mdi-logout" class="mr-2" @click="handleLogout">
      ログアウト
    </v-btn>
  </v-app-bar>

  <v-main>
    <v-container>
      <slot />
    </v-container>
  </v-main>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'

const auth = useAuthStore()
const router = useRouter()
const route = useRoute()
const drawer = ref(true)

const title = computed(() => route.meta.title || '備品管理システム')

function handleLogout() {
  auth.logout()
  router.push('/login')
}
</script>
