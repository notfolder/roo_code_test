import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "tests",
  use: {
    baseURL: process.env.PLAYWRIGHT_BASE_URL || "http://frontend:4173",
    headless: true,
    viewport: { width: 1280, height: 720 },
  },
});
