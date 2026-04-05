// @ts-check
const { defineConfig } = require('@playwright/test');

module.exports = defineConfig({
  testDir: './tests',
  timeout: 30000,
  retries: 0,
  use: {
    baseURL: 'http://frontend',
    headless: true,
  },
  reporter: [['list'], ['html', { open: 'never', outputFolder: 'playwright-report' }]],
});
