import { createRouter, createWebHistory } from "vue-router";
import LoginView from "../views/LoginView.vue";
import ItemListView from "../views/ItemListView.vue";
import UserAdminView from "../views/UserAdminView.vue";

const routes = [
  { path: "/login", component: LoginView },
  { path: "/items", component: ItemListView },
  { path: "/users", component: UserAdminView },
  { path: "/", redirect: "/items" },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("asset_token");
  if (to.path !== "/login" && !token) {
    return next({ path: "/login" });
  }
  if (to.path === "/login" && token) {
    return next({ path: "/items" });
  }
  next();
});

export default router;
