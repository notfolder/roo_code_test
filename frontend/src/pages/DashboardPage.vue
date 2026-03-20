<template>
  <v-app>
    <v-main>
      <v-container>
        <v-row class="mb-4">
          <v-col cols="12" class="d-flex justify-space-between align-center">
            <div class="text-h6">ダッシュボード</div>
            <div>
              <v-btn class="mr-2" color="primary" @click="go('/items')">備品一覧</v-btn>
              <v-btn class="mr-2" color="primary" @click="go('/reservations')">予約</v-btn>
              <v-btn class="mr-2" color="primary" @click="go('/overdue')">未返却</v-btn>
              <v-btn color="secondary" @click="go('/users')">アカウント</v-btn>
            </div>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()
const go = (path) => router.push(path)
</script>

<style scoped>
</style>
