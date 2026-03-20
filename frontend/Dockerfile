# 本番ビルド用マルチステージ
# 1. ビルドステージ: 依存インストール & Vite ビルド
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# 2. 配信ステージ: 軽量イメージで静的配信
FROM node:20-alpine
WORKDIR /app
RUN npm install -g serve
COPY --from=builder /app/dist ./dist
# 5173 ポートで dist を配信
CMD ["serve", "-s", "dist", "-l", "5173"]
