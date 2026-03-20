import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from '../pages/LoginPage.vue'
import DashboardPage from '../pages/DashboardPage.vue'
import ItemsPage from '../pages/ItemsPage.vue'
import ReservationsPage from '../pages/ReservationsPage.vue'
import OverduePage from '../pages/OverduePage.vue'
import UsersPage from '../pages/UsersPage.vue'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: LoginPage },
  { path: '/dashboard', component: DashboardPage },
  { path: '/items', component: ItemsPage },
  { path: '/reservations', component: ReservationsPage },
  { path: '/overdue', component: OverduePage },
  { path: '/users', component: UsersPage },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
