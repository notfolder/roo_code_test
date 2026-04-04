// Vue Router・未認証ガード・adminロールガード（共通処理）
import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import EquipmentListView from '../views/EquipmentListView.vue'
import EquipmentFormView from '../views/EquipmentFormView.vue'
import LendView from '../views/LendView.vue'
import ReturnView from '../views/ReturnView.vue'
import UserListView from '../views/UserListView.vue'
import UserFormView from '../views/UserFormView.vue'

const routes = [
  { path: '/', name: 'login', component: LoginView },
  { path: '/equipments', name: 'equipment-list', component: EquipmentListView, meta: { requiresAuth: true } },
  { path: '/equipments/new', name: 'equipment-create', component: EquipmentFormView, meta: { requiresAuth: true, requiresAdmin: true } },
  { path: '/equipments/:id/edit', name: 'equipment-edit', component: EquipmentFormView, meta: { requiresAuth: true, requiresAdmin: true } },
  { path: '/equipments/:id/lend', name: 'equipment-lend', component: LendView, meta: { requiresAuth: true, requiresAdmin: true } },
  { path: '/equipments/:id/return', name: 'equipment-return', component: ReturnView, meta: { requiresAuth: true, requiresAdmin: true } },
  { path: '/users', name: 'user-list', component: UserListView, meta: { requiresAuth: true, requiresAdmin: true } },
  { path: '/users/new', name: 'user-create', component: UserFormView, meta: { requiresAuth: true, requiresAdmin: true } },
  { path: '/users/:id/edit', name: 'user-edit', component: UserFormView, meta: { requiresAuth: true, requiresAdmin: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// ナビゲーションガード：未認証はログイン画面へ、staffはadmin専用ページへのアクセスを禁止する
router.beforeEach((to) => {
  const token = localStorage.getItem('access_token')
  const role = localStorage.getItem('user_role')

  if (to.meta.requiresAuth && !token) {
    return { name: 'login' }
  }
  if (to.meta.requiresAdmin && role !== 'admin') {
    return { name: 'equipment-list' }
  }
})

export default router
