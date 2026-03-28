/**
 * 認証ストア
 * ログイン状態・JWTトークン・ユーザー情報（ロール）を管理する
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import authApi from '../api/auth'

export const useAuthStore = defineStore('auth', () => {
  // JWTトークン（localStorageから初期値を読み込む）
  const token = ref(localStorage.getItem('access_token') || null)
  // ユーザーの役割（localStorageから初期値を読み込む）
  const role = ref(localStorage.getItem('role') || null)

  /** 管理担当者かどうか */
  const isAdmin = computed(() => role.value === 'admin')
  /** ログイン済みかどうか */
  const isLoggedIn = computed(() => token.value !== null)

  /** ログイン処理：APIを呼び出しトークンをlocalStorageに保存する */
  async function login(accountName, password) {
    const response = await authApi.login(accountName, password)
    token.value = response.data.access_token
    role.value = response.data.role
    localStorage.setItem('access_token', token.value)
    localStorage.setItem('role', role.value)
  }

  /** ログアウト処理：トークンをlocalStorageから削除する */
  async function logout() {
    try {
      await authApi.logout()
    } finally {
      token.value = null
      role.value = null
      localStorage.removeItem('access_token')
      localStorage.removeItem('role')
    }
  }

  return { token, role, isAdmin, isLoggedIn, login, logout }
})
