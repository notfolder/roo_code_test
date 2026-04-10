import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  { path: '/login', component: () => import('@/views/LoginView.vue'), meta: { public: true } },
  { path: '/', component: () => import('@/views/ItemListView.vue') },
  { path: '/items/manage', component: () => import('@/views/ItemManageView.vue'), meta: { admin: true } },
  { path: '/lend', component: () => import('@/views/LendView.vue'), meta: { admin: true } },
  { path: '/return', component: () => import('@/views/ReturnView.vue'), meta: { admin: true } },
  { path: '/history', component: () => import('@/views/HistoryView.vue') },
  { path: '/users', component: () => import('@/views/UserManageView.vue'), meta: { admin: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to) => {
  const authStore = useAuthStore()
  if (!to.meta.public && !authStore.isAuthenticated) {
    return '/login'
  }
  if (to.meta.admin && !authStore.isAdmin) {
    return '/'
  }
})

export default router
