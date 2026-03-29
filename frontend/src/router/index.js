import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/LoginView.vue'),
    meta: { requiresAuth: false },
  },
  {
    path: '/',
    name: 'Dashboard',
    component: () => import('../views/DashboardView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/loans/create',
    name: 'LoanCreate',
    component: () => import('../views/LoanCreateView.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/loans/return',
    name: 'LoanReturn',
    component: () => import('../views/ReturnCreateView.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/equipment',
    name: 'EquipmentList',
    component: () => import('../views/EquipmentListView.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/equipment/create',
    name: 'EquipmentCreate',
    component: () => import('../views/EquipmentFormView.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/equipment/:id/edit',
    name: 'EquipmentEdit',
    component: () => import('../views/EquipmentFormView.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/users',
    name: 'UserList',
    component: () => import('../views/UserListView.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/users/create',
    name: 'UserCreate',
    component: () => import('../views/UserFormView.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/reservations',
    name: 'ReservationList',
    component: () => import('../views/ReservationListView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/reservations/create',
    name: 'ReservationCreate',
    component: () => import('../views/ReservationCreateView.vue'),
    meta: { requiresAuth: true },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, _from, next) => {
  const token = localStorage.getItem('access_token')
  const user = JSON.parse(localStorage.getItem('user') || 'null')

  if (to.meta.requiresAuth && !token) {
    return next('/login')
  }
  if (to.meta.requiresAdmin && user?.role !== 'admin') {
    return next('/')
  }
  if (to.path === '/login' && token) {
    return next('/')
  }
  next()
})

export default router
