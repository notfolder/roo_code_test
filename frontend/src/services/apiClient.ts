import axios from "axios";

// API クライアント: Vite dev サーバでは /api をバックエンドへプロキシする前提
export const apiClient = axios.create({
  baseURL: "/api",
});

// リクエスト前に JWT を付与
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers = config.headers || {};
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
