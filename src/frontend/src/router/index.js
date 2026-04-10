import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import ItemListView from '../views/ItemListView.vue'
import LoginView from '../views/LoginView.vue'
import UserAdminView from '../views/UserAdminView.vue'

const routes = [
  { path: '/login', name: 'login', component: LoginView },
  { path: '/', name: 'items', component: ItemListView, meta: { requiresAuth: true } },
  { path: '/users', name: 'users', component: UserAdminView, meta: { requiresAuth: true, adminOnly: true } }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return { name: 'login' }
  }

  if (to.meta.adminOnly && !authStore.isAdmin) {
    return { name: 'items' }
  }

  if (to.name === 'login' && authStore.isAuthenticated) {
    return { name: 'items' }
  }

  return true
})

export default router
