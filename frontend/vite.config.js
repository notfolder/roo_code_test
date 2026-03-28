import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vuetify from 'vite-plugin-vuetify'

export default defineConfig({
  plugins: [
    vue(),
    // Vuetifyのスタイルを自動インポートする
    vuetify({ autoImport: true }),
  ],
  server: {
    // 開発時はバックエンドAPIにプロキシする
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
