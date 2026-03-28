/**
 * Vue Routerルーティング定義
 * ナビゲーションガードで未認証・権限不足のアクセスを制御する
 */
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/login',
    component: () => import('../views/LoginView.vue'),
    meta: { requiresAuth: false },
  },
  {
    path: '/',
    component: () => import('../views/EquipmentListView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/loans',
    component: () => import('../views/LoanManagementView.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/equipment',
    component: () => import('../views/EquipmentManagementView.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/accounts',
    component: () => import('../views/AccountManagementView.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  // 未定義のパスはトップにリダイレクトする
  { path: '/:pathMatch(.*)*', redirect: '/' },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// ナビゲーションガード：未認証・権限不足のアクセスを制御する
router.beforeEach((to) => {
  const token = localStorage.getItem('access_token')
  const role = localStorage.getItem('role')
  const isLoggedIn = token !== null

  // 認証が必要なページに未認証でアクセスした場合はログイン画面にリダイレクトする
  if (to.meta.requiresAuth && !isLoggedIn) {
    return '/login'
  }

  // 管理担当者専用ページに一般社員がアクセスした場合はトップにリダイレクトする
  if (to.meta.requiresAdmin && role !== 'admin') {
    return '/'
  }

  // ログイン済みでログイン画面にアクセスした場合はトップにリダイレクトする
  if (to.path === '/login' && isLoggedIn) {
    return '/'
  }
})

export default router
