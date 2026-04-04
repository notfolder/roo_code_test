# ステージ1: npmビルド
FROM node:20-alpine AS builder

WORKDIR /app
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm run build

# ステージ2: nginxで配信
FROM nginx:alpine

# ビルド成果物をnginxの配信ディレクトリにコピー
COPY --from=builder /app/dist /usr/share/nginx/html

# nginxの設定をコピー
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
