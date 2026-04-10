<template>
  <v-app>
    <v-app-bar color="primary" dark>
      <v-toolbar-title>備品貸出管理</v-toolbar-title>
      <v-spacer />
      <template v-if="isLoggedIn">
        <v-btn text :to="'/items'">備品一覧</v-btn>
        <v-btn text v-if="isAdmin" :to="'/users'">ユーザー管理</v-btn>
        <v-btn text @click="logout">ログアウト</v-btn>
      </template>
    </v-app-bar>
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script setup>
import { computed } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

const token = computed(() => localStorage.getItem("asset_token"));
const role = computed(() => localStorage.getItem("asset_role"));
const isLoggedIn = computed(() => Boolean(token.value));
const isAdmin = computed(() => role.value === "admin");

const logout = () => {
  localStorage.removeItem("asset_token");
  localStorage.removeItem("asset_role");
  localStorage.removeItem("asset_user");
  router.push("/login");
};
</script>
