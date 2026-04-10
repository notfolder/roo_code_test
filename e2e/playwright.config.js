import { defineConfig } from '@playwright/test'

export default defineConfig({
  testDir: './tests',
  timeout: 90_000,
  expect: {
    timeout: 10_000
  },
  retries: 1,
  use: {
    baseURL: process.env.BASE_URL || 'http://frontend',
    headless: true
  }
})
