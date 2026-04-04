import { createContext, useContext, useState, useEffect, ReactNode } from 'react'
import { apiClient, setAuthToken, clearAuthToken } from '../api/client'
import type { User } from '../types'

interface AuthContextType {
  user: User | null
  token: string | null
  login: (email: string, password: string) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextType | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [token, setToken] = useState<string | null>(() => localStorage.getItem('auth_token'))

  useEffect(() => {
    if (token) {
      // トークンがある場合はユーザー情報を取得
      apiClient.get<User>('/auth/me').then((res) => {
        setUser(res.data)
      }).catch(() => {
        clearAuthToken()
        setToken(null)
        setUser(null)
      })
    }
  }, [])

  const login = async (email: string, password: string) => {
    const res = await apiClient.post<{ token: string; user: User }>('/auth/login', { email, password })
    const { token: newToken, user: newUser } = res.data
    setAuthToken(newToken)
    setToken(newToken)
    setUser(newUser)
  }

  const logout = () => {
    clearAuthToken()
    setToken(null)
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, token, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}
