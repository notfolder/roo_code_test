import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// BACKEND URL は環境変数で上書き可能（Docker: http://backend:3000, ローカル: http://localhost:3000）
const backend = process.env.VITE_BACKEND_URL || "http://localhost:3000";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    host: "0.0.0.0",
    proxy: {
      "/api": {
        target: backend,
        changeOrigin: true,
      },
    },
  },
});
