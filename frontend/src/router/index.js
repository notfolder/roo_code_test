import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import EquipListView from '../views/EquipListView.vue'
import ReservationsView from '../views/ReservationsView.vue'
import LendReturnView from '../views/LendReturnView.vue'
import AdminMenuView from '../views/AdminMenuView.vue'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: LoginView },
  { path: '/equipments', component: EquipListView },
  { path: '/reservations', component: ReservationsView },
  { path: '/lend-return', component: LendReturnView },
  { path: '/admin', component: AdminMenuView },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
