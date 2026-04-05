import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'

import EquipmentList from '../pages/EquipmentList.vue'
import LoginPage from '../pages/LoginPage.vue'
import EquipmentManagement from '../pages/EquipmentManagement.vue'
import LendingNew from '../pages/LendingNew.vue'
import LendingReturn from '../pages/LendingReturn.vue'
import LendingHistory from '../pages/LendingHistory.vue'

const routes = [
  { path: '/', component: EquipmentList },
  { path: '/login', component: LoginPage },
  { path: '/equipment', component: EquipmentManagement, meta: { requiresAuth: true } },
  { path: '/lending/new', component: LendingNew, meta: { requiresAuth: true } },
  { path: '/lending/return', component: LendingReturn, meta: { requiresAuth: true } },
  { path: '/lending/history', component: LendingHistory, meta: { requiresAuth: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// ナビゲーションガード: 認証が必要な画面は未認証時にログイン画面にリダイレクトする
router.beforeEach((to) => {
  const authStore = useAuthStore()
  if (to.meta.requiresAuth && !authStore.isLoggedIn) {
    return '/login'
  }
})

export default router
